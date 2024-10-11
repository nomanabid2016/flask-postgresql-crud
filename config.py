from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DBConfig(BaseSettings):
    CONNECTION_STR: str
    POOL_SIZE: str = 100

    class Config:
        env_prefix = "DB_"


class Logging(BaseSettings):
    LEVEL: int = 20

    class Config:
        env_prefix = "LOG_"


class Config:
    DB = DBConfig()
    LOG = Logging()