import os
from pydantic_settings import BaseSettings
from decouple import config
from pathlib import Path

class Settings(BaseSettings):

    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_SERVER : str 
    POSTGRES_PORT : str = "5432"
    POSTGRES_DB : str
    
    @property
    def DATABASE_URL(self):
        f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()