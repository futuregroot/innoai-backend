from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from app.extensions import db, cors, cache, bcrypt, limiter, csrf, login_manager
from flask_wtf.csrf import CSRFError
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.mongo_repository import MongoRepository
from app.services.ingestion_service import IngestionService

def create_app(config_name):
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/"
    )
    app.app_context().push()

    app.config.from_object(config_name)

    db.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    from app import models
    db.create_all()

    # Initialize ChromaRepository
    chroma_repo = ChromaRepository()
    app.config['CHROMA_REPO'] = chroma_repo

    # Initialize MongoRepository
    mongo_repo = MongoRepository()
    app.config['MONGO_REPO'] = mongo_repo

    ingestion_service = IngestionService()
    ingestion_service.visualize_embeddings_with_tensorboard(collection_name="vehicle_collection",
                                                            log_dir="tensorboard_logs")

    print(f"ChromaDB data is stored in: {chroma_repo.get_local_storage_path()}")

    from app.routes.auth import auth_bp
    from app.routes import api_bp, pages_bp
    from app.routes.api.ingestion import ingestion_bp
    from app.routes.api.tests import tests_bp
    from app.routes.api.chatbot import chatbot_bp
    from app.routes.api.chat_history import chat_history_bp
    from app.routes.api.chatroom import chatroom_bp  # Import the chatroom blueprint

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(ingestion_bp)
    app.register_blueprint(tests_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(chat_history_bp)
    app.register_blueprint(chatroom_bp)  # Register the chatroom blueprint

    app.before_request(lambda: limiter.check())

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        response = jsonify({"message": "CSRF token is missing or invalid"})
        response.status_code = 400
        return response

    return app
