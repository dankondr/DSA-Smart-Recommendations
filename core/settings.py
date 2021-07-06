from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = 'DSA Smart'
    app_host: str = '0.0.0.0'
    app_port: int = 3000

    debug: bool = False
    timeout_keep_alive: int = 15

    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_max_conn: int = 5

    cors_allowed_origins: list[str] = ['*']

    class Config:
        allow_mutation = False


settings: Settings = Settings()
