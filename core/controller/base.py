from typing import Any, Generic, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel

from core.exceptions import NotFoundException
from core.repository import BaseRepository
from app.models.user import User


class BaseController():
    """Base class for data controllers."""

    def __init__(self, model: Any, repository: BaseRepository):
        self.model_class = model
        self.repository = repository

    def get_by_id(
        self, id:int | None = None
    ) -> list[Any]:
        """
        Returns a list of records.

        :param join_: The joins to make.
        :return: A list of records.
        """
        query = {"id": id}
        response = self.repository.find_all(query)
        return response
    
    def get_all(self):
        return self.repository.find_all()