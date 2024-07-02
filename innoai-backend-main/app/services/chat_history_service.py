import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ChatHistoryService")

class ChatHistoryService:
    def __init__(self, mongo_repo):
        self.logger = logging.getLogger("ChatHistoryService")
        self.mongo_repo = mongo_repo

    def save_history(self, user_id, chat_history):
        self.logger.debug(f"Saving chat history for user_id: {user_id}")
        return self.mongo_repo.save_chat_history(user_id, chat_history)

    def get_history(self, user_id):
        self.logger.debug(f"Retrieving chat history for user_id: {user_id}")
        return self.mongo_repo.get_chat_history(user_id)
