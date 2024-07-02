import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MongoRepository")

class MongoRepository:
    def __init__(self):
        self.logger = logging.getLogger("MongoRepository")
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client.innoai
        self.chatroom_collection = self.db.chatroom
        self.chat_history_collection = self.db.chathistory

    def save_chat_history(self, user_id, chat_history):
        self.logger.debug(f"Saving chat history for user_id: {user_id}")
        record = {
            "user_id": user_id,
            "chat_history": chat_history
        }
        result = self.chat_history_collection.insert_one(record)
        return str(result.inserted_id)

    def get_chat_history(self, user_id):
        self.logger.debug(f"Retrieving chat history for user_id: {user_id}")
        history = self.chat_history_collection.find_one({"user_id": user_id}, {"_id": 0, "chat_history": 1})
        if history:
            return history.get('chat_history', [])
        else:
            return []

    def create_chatroom(self, user_id):
        self.logger.debug(f"Creating chatroom for user_id: {user_id}")
        chatroom_id = str(uuid4())
        record = {
            "user_id": user_id,
            "chatroom_id": chatroom_id,
            "messages": []
        }
        self.chatroom_collection.insert_one(record)
        return chatroom_id

    def get_chatroom(self, user_id):
        self.logger.debug(f"Retrieving chatroom for user_id: {user_id}")
        chatroom = self.chatroom_collection.find_one({"user_id": user_id}, {"_id": 0})
        if chatroom:
            return chatroom
        else:
            return None

    def update_chatroom(self, chatroom_id, user_message, chatbot_message):
        self.logger.debug(f"Updating chatroom for chatroom_id: {chatroom_id}")
        updated_date = datetime.utcnow().isoformat()
        new_message = {
            "user": user_message,
            "chatbot": chatbot_message,
            "updatedDate": updated_date
        }
        result = self.chatroom_collection.update_one(
            {"chatroom_id": chatroom_id},
            {"$push": {"messages": new_message}}
        )
        return result.modified_count > 0
