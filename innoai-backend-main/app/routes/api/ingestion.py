from flask import Blueprint, request, jsonify
from app.services.ingestion_service import IngestionService
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("IngestionAPI")

ingestion_bp = Blueprint("ingestion", __name__, url_prefix="/ingestion")
logger.debug("Ingestion Blueprint Created")

# Initialize IngestionService
ingestion_service = IngestionService()
logger.debug("Ingestion Service Initialized")

PDF_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'external_resources', 'pdfs'))

@ingestion_bp.route("/ingest/<string:file>", methods=["POST"])
def ingest_pdf(file):
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        file_path = os.path.join(PDF_DIRECTORY, file)
        logger.debug(f"File path constructed: {file_path}")
        result = ingestion_service.process_pdf(file_path, collection_name)
        logger.debug(f"Ingestion result: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in ingest_pdf: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/ingest-all", methods=["POST"])
def ingest_all_pdfs():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        logger.debug(f"Directory path: {PDF_DIRECTORY}")
        result = ingestion_service.process_all_pdfs_in_directory(PDF_DIRECTORY, collection_name)
        logger.debug(f"Ingestion of all PDFs result: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in ingest_all_pdfs: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/ingest-text", methods=["POST"])
def ingest_text():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        text = data.get("text")
        result = ingestion_service.process_text(text, collection_name)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in ingest_text: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/ingest-semantic-chunk", methods=["POST"])
def ingest_semantic_chunk():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        text = data.get("text")
        result = ingestion_service.process_semantic_chunks(text, collection_name)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in ingest_semantic_chunk: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/ingest-token-text-split", methods=["POST"])
def ingest_token_text_split():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        text = data.get("text")
        result = ingestion_service.process_token_text_splitter(text, collection_name)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in ingest_token_text_split: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/delete-collection", methods=["POST"])
def delete_collection():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        result = ingestion_service.delete_collection(collection_name)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in delete_collection: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/delete-all-collections", methods=["POST"])
def delete_all_collections():
    try:
        result = ingestion_service.delete_all_collections()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in delete_all_collections: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/search", methods=["POST"])
def search():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        query = data.get('query')
        result = ingestion_service.search(query, collection_name)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ingestion_bp.route("/get-all-data", methods=["POST"])
def get_all_data():
    try:
        data = request.get_json()
        collection_name = data.get('collection_name')
        if not collection_name:
            return jsonify({"error": "Missing collection_name in request body"}), 400

        all_data = ingestion_service.get_all_data(collection_name)
        return jsonify(all_data), 200
    except Exception as e:
        logger.error(f"Error in get_all_data: {str(e)}")
        return jsonify({"error": str(e)}), 500