from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str

    class Config:
        env_file = '.env'

settings = Settings()