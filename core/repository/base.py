from ..database.dbClient import MongoDBClient
import os

class BaseRepository():
    def __init__(self, db_client: MongoDBClient, collection_name):
        self.db_client = db_client
        self.collection = db_client.get_db[collection_name]

    def insert_document(self, document):
        if self.collection is not None:
            return self.collection.insert_one(document).inserted_id

    def find_document(self, query=None):
        if query is None:
            query = {}
        if self.collection is not None:
            return self.collection.find_one(query)
    
    
    def find_all(self, query=None):
        if query is None:
            query = {}
        if self.collection is not None:
            return self.collection.find(query)

    @property
    def get_collection(self):
        return self.collection

    @get_collection.setter
    def set_collection(self, collection_name):
        self.collection = self.db_client.get_db[collection_name]
