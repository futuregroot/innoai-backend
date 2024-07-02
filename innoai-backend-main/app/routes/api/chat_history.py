from flask import Blueprint, request, jsonify
from app.services.chat_history_service import ChatHistoryService
from app.repositories.mongo_repository import MongoRepository
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ChatHistoryAPI")

chat_history_bp = Blueprint("chat_history", __name__, url_prefix="/chat_history")
logger.debug("ChatHistory Blueprint Created")

mongo_repo = MongoRepository()
chat_history_service = ChatHistoryService(mongo_repo)

@chat_history_bp.route('/save-chat-history', methods=['POST'])
def save_history():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        chat_history = data.get('chat_history')

        if not user_id or not chat_history:
            return jsonify({"error": "User ID and chat history are required"}), 400

        result = chat_history_service.save_history(user_id, chat_history)

        return jsonify({"result": result}), 200

    except Exception as e:
        logger.error(f"Error in save_history: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chat_history_bp.route('/get-chat-history', methods=['POST'])
def get_history():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        history = chat_history_service.get_history(user_id)

        return jsonify({"history": history}), 200

    except Exception as e:
        logger.error(f"Error in get_history: {str(e)}")
        return jsonify({"error": str(e)}), 500
