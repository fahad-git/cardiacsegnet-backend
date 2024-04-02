from pydantic import EmailStr

from app.models.user import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.controller import BaseController
# from core.database import Propagation, Transactional
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTHandler, PasswordHandler

class AuthController(BaseController):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    # @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, name: str, username: str, email: EmailStr, password: str) -> User:
        # Check if user exists with email
        user = self.user_repository.get_by_email(email)

        if user:
            raise BadRequestException("User already exists with this email")

        # Check if user exists with username
        user = self.user_repository.get_by_username(username)

        if user:
            raise BadRequestException("User already exists with this username")

        password = PasswordHandler.hash(password)

        newUser = dict({
                'uuid': 'user 1',
                'email': email,
                'password': password,
                'username': username,
                'name': name
            })

        newUser["_id"] = self.user_repository.create_user(newUser)
        return newUser

    async def login(self, email: EmailStr, password: str) -> Token:
        user =  self.user_repository.get_by_email(email)
        if not user:
            raise UnauthorizedException("Invalid credentials")
        if not PasswordHandler.verify(user["password"], password):
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user["uuid"]}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )
