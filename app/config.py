from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"
    DATABASE_URL: str = "sqlite:///./campus.db"
    UPLOAD_DIR: str = "storage/uploads"
    CAMPUS_EMAIL_DOMAIN: str = "@college.edu"

    class Config:
        env_file = ".env"

settings = Settings()
