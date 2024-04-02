from fastapi import Depends, Request

from app.controllers.user import UserController
from core.exceptions.base import UnauthorizedException
from core.factory import Factory


def get_current_user(
    request: Request,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    if(request.user.id is None):
        raise UnauthorizedException("Invalid user token")
    return user_controller.get_user_by_id(request.user.id)
