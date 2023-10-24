from enum import Enum
from pydantic_settings import BaseSettings

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True


class Config(BaseConfig):
    DEBUG: int = 0
    DEFAULT_LOCALE: str = "en_US"
    ENVIRONMENT: str = EnvironmentType.DEVELOPMENT
    MONGODB_URL: str = "mongodb+srv://srdan:filipovic@acsp.jyqsecl.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_URL_LOCAL: str = 'mongodb://localhost:27017/'
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    RELEASE_VERSION: str = "0.1"
    SECRET_KEY: str = "super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    CELERY_BROKER_URL: str = "amqp://rabbit:password@localhost:5672"
    CELERY_BACKEND_URL: str = "redis://localhost:6379/0"

config: Config = Config()
