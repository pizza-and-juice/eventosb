from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_SECRET_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def CA_CERT_PATH(self) -> Path:
        return Path(__file__).parent.parent / "certs" / "ca-certificate.crt"
    
    @property
    def SECRET_KEY(self) -> str:
        return self.JWT_SECRET_KEY

    class Config:
        env_file = ".env"


settings = Settings()
