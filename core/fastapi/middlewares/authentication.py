from typing import Optional, Tuple
from fastapi import Depends

from jose import JWTError, jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection
from app.models.user import User

from app.schemas.extras.current_user import CurrentUser
from core.config import config
from core.fastapi.dependencies.current_user import get_current_user


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, 
        conn: HTTPConnection
    ) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
        except JWTError:
            return False, current_user

        current_user.id = user_id
        return True, current_user

class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
