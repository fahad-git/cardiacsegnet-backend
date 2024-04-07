import pymongo

class MongoDBClient:
    def __init__(self, connection_uri, db_name):
        self.connection_uri = connection_uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def open_connection(self):
        try:
            self.client = pymongo.MongoClient(self.connection_uri)
            self.db = self.client[self.db_name]
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def close_connection(self):
        if self.client:
            self.client.close()

    @property
    def is_connected(self):
        return self.client is not None

    @property
    def get_db(self):
        return self.db
    



# if db_client.is_connected:
#     print("Connected to MongoDB")
#     user_handler = DocumentHandler(db_client, "User")
#     data_handler = DocumentHandler(db_client, "Data")

#     def get_user_handler():
#         return user_handler

#     def get_data_handler():
#         return data_handler
