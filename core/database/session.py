from contextvars import ContextVar, Token
from typing import Union
from .dbClient import MongoDBClient
from typing import Any
import os

session_context: ContextVar[MongoDBClient] = ContextVar("session_context")

def get_session_context() -> MongoDBClient:
    # return session_context.get()
     db_client = MongoDBClient(os.getenv("MONGODB_URL"), "ACSP")
     db_client.open_connection()
     return db_client


def set_session_context(sessionClient: MongoDBClient) -> MongoDBClient:
    return session_context.set(sessionClient)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)



async def get_session() -> MongoDBClient:
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    try:
        yield get_session_context()
    finally:
        # get_session_context()
        print("Exception occured")
