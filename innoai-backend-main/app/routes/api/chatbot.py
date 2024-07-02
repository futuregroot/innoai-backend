from flask import Blueprint, request, jsonify
from app.services.answer_gpt_service import AnswerGPTService
from app.services.split_gpt_service import SplitGPTService
from app.services.ingestion_service import IngestionService
from app.services.chatroom_service import ChatroomService  # Import the chatroom service
from app.repositories.mongo_repository import MongoRepository
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ChatbotAPI")

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/chatbot")
logger.debug("Chatbot Blueprint Created")

if not os.getenv("OPENAI_API_KEY"):
    logger.error("The OPENAI_API_KEY environment variable is not set.")
    raise EnvironmentError("Missing OPENAI_API_KEY environment variable.")

answer_gpt_service = AnswerGPTService()
split_gpt_service = SplitGPTService()
ingestion_service = IngestionService()
mongo_repo = MongoRepository()
chatroom_service = ChatroomService(mongo_repo)

def format_search_results(results):
    context = f"Document ID: {results['id']}\nMetadata: {results['metadata']}\nContent: {results['document']}"
    return context

@chatbot_bp.route("/split", methods=["POST"])
def split_question():
    try:
        data = request.get_json()
        model = data.get('model')
        question = data.get('question')

        if not question:
            return jsonify({"error": "Question is required"}), 400

        if model == 'gpt-3.5-turbo':
            logger.debug(f"Splitting question with GPT model: {question}")
            result = split_gpt_service.split(model, question)
        elif model == 'llama':
            logger.debug(f"Splitting question with LLama model: {question}")
            result = split_llama_service.split(model, question)
        else:
            return jsonify({"error": "Unsupported model"}), 400

        logger.debug(f"Split result: {result}")
        return jsonify({"result": result}), 200

    except Exception as e:
        logger.error(f"Error in split_question: {str(e)}")
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route("/answer", methods=["POST"])
def answer_question():
    try:
        data = request.get_json()
        model = data.get('model')
        question = data.get('question')
        chat_history = data.get('chat_history', '')
        collection_name = data.get('collection_name', 'vehicle_collection')
        chatroom_id = data.get('chatroom_id')

        if not question or not chatroom_id:
            return jsonify({"error": "Question and chatroom ID are required"}), 400
        if not model:
            return jsonify({"error":"Model Information is required"}), 400

        logger.debug(f"Searching for context with query: {question}")
        search_results = ingestion_service.search(question, collection_name)

        if 'error' in search_results:
            return jsonify(search_results), 500

        formatted_context = format_search_results(search_results['results'])

        logger.debug(f"Answering question with GPT model: {question}")
        answer = answer_gpt_service.answer(
            model, question, chat_history, formatted_context, chatroom_service, chatroom_id
        )

        return jsonify({
            "id": search_results['results']['id'],
            "document": search_results['results']['document'],
            "metadata": search_results['results']['metadata'],
            "answer": answer
        }), 200

    except Exception as e:
        logger.error(f"Error in answer_question: {str(e)}")
        return jsonify({"error": str(e)}), 500
