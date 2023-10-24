from http import HTTPStatus
from typing import Any
from fastapi import Depends, Request, HTTPException
from fastapi import Depends, HTTPException
from app.controllers.user import UserController
from core.exceptions import CustomException
from core.factory import Factory
from starlette.status import HTTP_403_FORBIDDEN

# from core.security.access_control import (
#     AccessControl,
#     Authenticated,
#     Everyone,
#     RolePrincipal,
#     UserPrincipal,
# )


class InsufficientPermissionsException(CustomException):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = "Insufficient permissions"


async def get_user_principals(
    request: Request,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> list:
    # user_id = request.user.id
    # principals = [Everyone]

    # if not user_id:
    #     return principals

    # user = await user_controller.get_by_id(id_=user_id)

    # principals.append(Authenticated)
    # principals.append(UserPrincipal(user.id))

    # if user.is_admin:
    #     principals.append(RolePrinipal("admin"))

    # return principals
    return None

default_exception = HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Forbidden")

class AccessControl:
    def __init__(
        self,
        user_principals_getter: Any,
        permission_exception: Any = default_exception,
    ) -> None:
        self.user_principals_getter = user_principals_getter
        self.permission_exception = permission_exception


    def __call__(self, permissions: str):
        def _permission_dependency():
            return None

        return _permission_dependency

    def assert_access(self, principals: list, permissions: str, resource: Any):
            raise True
    
Permissions = AccessControl(
    user_principals_getter=get_user_principals,
    permission_exception=InsufficientPermissionsException,
)