from app.models import User
from core.repository import BaseRepository
import asyncio
from core.database.session import get_session_context

class UserRepository(BaseRepository):
    """
    User repository provides all the database operations for the User model.
    """

    def __init__(self):
        self.db_client = get_session_context()
        super().__init__(self.db_client, "User")
        self.user_handler = BaseRepository(self.db_client, "User")

    def create_user(self, user: User) -> User | None:
        """
        Create new user in database.

        :return: User

        """
        return self.user_handler.insert_document(user)

    def get_all_users(self) -> list[User] | None:
        """
        Get all users.

        :return: List[User]

        """
        return self.user_handler.find_all()

    def get_by_username(
        self, username: str | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        query = {"username": username}
        return self.user_handler.find_document(query)

    def get_by_email(
        self, email: str | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = {"email": email}
        return self.user_handler.find_document(query)
    
    def get_by_id(
        self, id: str | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = {"uuid": id}
        return self.user_handler.find_document(query)