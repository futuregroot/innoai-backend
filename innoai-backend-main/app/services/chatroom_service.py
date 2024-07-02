import logging
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ChatroomService")

class ChatroomService:
    def __init__(self, mongo_repo):
        self.logger = logging.getLogger("ChatroomService")
        self.mongo_repo = mongo_repo

    def create_chatroom(self, user_id):
        self.logger.debug(f"Creating chatroom for user_id: {user_id}")
        return self.mongo_repo.create_chatroom(user_id)

    def get_chatroom(self, user_id):
        self.logger.debug(f"Retrieving chatroom for user_id: {user_id}")
        return self.mongo_repo.get_chatroom(user_id)

    def update_chatroom_message(self, chatroom_id, user_message, chatbot_message):
        self.logger.debug(f"Updating chatroom for chatroom_id: {chatroom_id}")
        return self.mongo_repo.update_chatroom(chatroom_id, user_message, chatbot_message)
