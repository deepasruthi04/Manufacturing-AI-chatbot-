from pymongo import MongoClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(settings.MONGO_URI)
        
    def get_database(self, db_name: str):
        return self.client[db_name]

mongodb_client = MongoDB()
