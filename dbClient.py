import pymongo


class MongoDBClient:
    def __init__(self, token, db):
        self.__token = token
        self.__dbName = db
        self.__client = None
        self.__db = None

    def open_connection(self):
        self.__client = pymongo.MongoClient(self.__token)
        self.__db = self.__client[self.__dbName]

    def close_connection(self):
        if self.__client:
            self.__client.close()

    @property
    def db(self):
        return self.__db


class DocumentHandler:
    def __init__(self, db_client, coll):
        self.__db_client = db_client
        self.__collection = db_client.db[coll]

    def insert_document(self, document):
        self.__collection.insert_one(document)

    def find_document(self, query=None):
        if query is None:
            query = {}
        return self.__collection.find_one(query)

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, coll):
        self.__collection = coll

db_client = MongoDBClient("mongodb+srv://srdan:filipovic@acsp.jyqsecl.mongodb.net/?retryWrites=true&w=majority", "ACSP")
user_handler = DocumentHandler(db_client, "User")
data_handler = DocumentHandler(db_client, "Data")

def get_user_handler():
    return user_handler

def get_data_handler():
    return data_handler
