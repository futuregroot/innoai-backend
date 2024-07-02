from flask import Blueprint, request, jsonify
from app.services.chatroom_service import ChatroomService
from app.repositories.mongo_repository import MongoRepository
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ChatroomAPI")

chatroom_bp = Blueprint("chatroom", __name__, url_prefix="/chatroom")
logger.debug("Chatroom Blueprint Created")

mongo_repo = MongoRepository()
chatroom_service = ChatroomService(mongo_repo)

@chatroom_bp.route('/create-chatroom', methods=['POST'])
def create_chatroom():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        chatroom_id = chatroom_service.create_chatroom(user_id)
        return jsonify({"chatroom_id": chatroom_id}), 200

    except Exception as e:
        logger.error(f"Error in create_chatroom: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chatroom_bp.route('/get-chatroom', methods=['POST'])
def get_chatroom():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        chatroom = chatroom_service.get_chatroom(user_id)
        return jsonify({"chatroom": chatroom}), 200

    except Exception as e:
        logger.error(f"Error in get_chatroom: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chatroom_bp.route('/update-chatroom', methods=['POST'])
def update_chatroom():
    try:
        data = request.get_json()
        chatroom_id = data.get('chatroom_id')
        user_message = data.get('user_message')
        chatbot_message = data.get('chatbot_message')

        if not chatroom_id or not user_message or not chatbot_message:
            return jsonify({"error": "Chatroom ID, user message, and chatbot message are required"}), 400

        success = chatroom_service.update_chatroom_message(chatroom_id, user_message, chatbot_message)
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"error": "Failed to update chatroom"}), 500

    except Exception as e:
        logger.error(f"Error in update_chatroom: {str(e)}")
        return jsonify({"error": str(e)}), 500
