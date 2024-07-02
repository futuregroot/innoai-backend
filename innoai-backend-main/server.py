import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
import subprocess
import signal

# Initialize colorama
init(autoreset=True)

# Load the common .env file
load_dotenv()

# Load additional environment-specific configurations
env = os.getenv('ENV', 'local')
if env == 'local':
    load_dotenv('.env.local')
    env_color = Fore.GREEN
elif env == 'development':
    load_dotenv('.env.dev')
    env_color = Fore.YELLOW
elif env == 'production':
    load_dotenv('.env.production')
    env_color = Fore.RED
else:
    env_color = Fore.WHITE

# Print the environment
print(f"{env_color}Running in {env} environment{Style.RESET_ALL}")

# Import and create the Flask app after loading environment variables
from app import create_app

config_name = os.getenv('FLASK_CONFIG', 'app.config.local.LocalConfig')
app = create_app(config_name)


def start_tensorboard(logdir, port=6006):
    """Start TensorBoard as a subprocess."""
    tensorboard_command = ["tensorboard", f"--logdir={logdir}", f"--port={port}"]
    return subprocess.Popen(tensorboard_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
    debug = config_name != 'app.config.prod.ProdConfig'
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tensorboard_logs'))

    # Ensure log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    tensorboard_process = start_tensorboard(logdir=log_dir)

    try:
        app.run(host='0.0.0.0', port=5000, debug=debug)
    except KeyboardInterrupt:
        print("Keyboard Interrupt received, shutting down gracefully.")
    finally:
        if tensorboard_process:
            tensorboard_process.send_signal(signal.SIGINT)
            tensorboard_process.wait()
            print("TensorBoard process terminated.")
        print("Cleanup complete. Exiting now.")
