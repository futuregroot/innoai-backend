import logging
import os
from chromadb import PersistentClient
from chromadb.config import Settings


class ChromaRepository:
    def __init__(self, collection_name="vehicle_collection", embedding_dim=768):
        self.logger = logging.getLogger("ChromaRepository")
        self.use_local = os.getenv("USE_LOCAL_CHROMA_DB", "True") == "True"
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim

        if self.use_local:
            self.chroma_storage_path = os.getenv("LOCAL_CHROMA_DB_PATH", "chroma_storage")
        else:
            chroma_db_ip = os.getenv("CHROMA_DB_IP")
            chroma_db_port = os.getenv("CHROMA_DB_PORT")
            chroma_db_path = os.getenv("CHROMA_DB_PATH")
            self.chroma_storage_path = f"http://{chroma_db_ip}:{chroma_db_port}{chroma_db_path}"

        self._initialize_client()
        self.collection = None
        self._ensure_collection_exists()

    def _initialize_client(self):
        try:
            if self.use_local:
                if not os.path.exists(self.chroma_storage_path):
                    os.makedirs(self.chroma_storage_path)
                self.client = PersistentClient(
                    path=self.chroma_storage_path,
                    settings=Settings()
                )
                self.logger.info(f"ChromaDB client initialized with path: {self.chroma_storage_path}")
            else:
                self.logger.error("Remote ChromaDB initialization not implemented.")
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB client: {str(e)}")
            self.client = None

    def _ensure_collection_exists(self):
        if not self.client:
            self.logger.error("ChromaDB client is not initialized.")
            return
        try:
            self.collection = self.client.get_collection(self.collection_name)
            self.logger.info(f"Collection '{self.collection_name}' retrieved successfully")
        except Exception as e:
            self.logger.info(f"Collection '{self.collection_name}' does not exist. Creating new collection.")
            self._create_collection()

    def _create_collection(self):
        try:
            self.collection = self.client.create_collection(
                name=self.collection_name
            )
            self.logger.info(f"Created collection '{self.collection_name}'")
        except Exception as e:
            self.collection = None
            self.logger.error(f"Failed to create collection '{self.collection_name}': {e}")

    def delete_collection(self, collection_name):
        if not self.client:
            self.logger.error("ChromaDB client is not initialized.")
            return
        try:
            self.logger.info(f"Attempting to delete collection '{collection_name}'")
            self.client.delete_collection(name=collection_name)
            self.logger.info(f"Successfully deleted collection '{collection_name}'")
        except Exception as e:
            self.logger.error(f"Could not delete collection '{collection_name}': {e}")

    def delete_all_collections(self):
        if not self.client:
            self.logger.error("ChromaDB client is not initialized.")
            return
        try:
            self.logger.info(f"Attempting to delete all collections")
            collections = self.client.list_collections()
            for collection in collections:
                self.client.delete_collection(name=collection['name'])
                self.logger.info(f"Successfully deleted collection '{collection['name']}'")
            self.logger.info(f"All collections deleted successfully")
        except Exception as e:
            self.logger.error(f"Could not delete all collections: {e}")

    def upsert_data(self, documents, embeddings, ids, metadata):
        if not self.collection:
            self.logger.error("Collection is not initialized.")
            return
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadata,
                documents=documents
            )
            self.logger.info(f"Data upserted successfully: {documents}, with IDs: {ids} and metadata: {metadata}")
        except Exception as e:
            self.logger.error(f"An error occurred while upserting data: {e}")

    def query_data(self, query_embedding, n_results=5):
        if not self.collection:
            self.logger.error("Collection is not initialized.")
            return None
        try:
            results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
            self.logger.info(f"Query results: {results}")
            return results
        except Exception as e:
            self.logger.error(f"An error occurred while querying data: {e}")
            return None

    def get_all_data(self):
        if not self.collection:
            self.logger.error("Collection is not initialized.")
            return None
        try:
            all_data = self.collection.query(query_texts=["*"], n_results=1000)
            self.logger.info(f"All data in the collection: {all_data}")
            return {"results": all_data}
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving all data: {e}")
            return {"results": []}

    def get_local_storage_path(self):
        self.logger.info(f"ChromaDB Storage Path: {self.chroma_storage_path}")
        return self.chroma_storage_path