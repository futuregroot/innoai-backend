import chromadb
import logging
import os
from dotenv import load_dotenv

# Conditional loading of environment-specific variables
load_dotenv()  # Load default .env

env = os.getenv('ENV', 'local')  # Default to 'local' if not set
if env == 'local':
    load_dotenv('.env.local')
elif env == 'development':
    load_dotenv('.env.dev')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_chroma_db_client():
    use_local = os.getenv("USE_LOCAL_CHROMA_DB", "False").lower() == "true"
    if use_local:
        chroma_db_path = os.getenv("LOCAL_CHROMA_DB_PATH")
        logger.info(f"Using local Chroma DB at {chroma_db_path}")

        # Ensure directory exists
        dir_path = os.path.dirname(chroma_db_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # Ensure the DB is not reinitialized
        if not os.path.exists(chroma_db_path):
            chroma_db = chromadb.PersistentClient(path=chroma_db_path)
        else:
            chroma_db = chromadb.PersistentClient(path=chroma_db_path)

    else:
        chroma_db_host = os.getenv("CHROMA_DB_IP")
        chroma_db_port = os.getenv("CHROMA_DB_PORT")
        chroma_db = chromadb.Client()
        chroma_db.host = chroma_db_host
        chroma_db.port = chroma_db_port
        logger.info(f"Using remote Chroma DB at {chroma_db_host}:{chroma_db_port}")

    return chroma_db

# Example usage
if __name__ == "__main__":
    client = get_chroma_db_client()
    logger.info("Chroma DB Client initialized.")