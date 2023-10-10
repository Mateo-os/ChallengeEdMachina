from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_SERVER : str 
    POSTGRES_PORT : str = "5432"
    POSTGRES_DB : str
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()