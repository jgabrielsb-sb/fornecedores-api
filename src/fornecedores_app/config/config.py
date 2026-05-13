from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

import os

def get_env_file() -> str:
    app_env = os.getenv("APP_ENV", "dev")

    if app_env == "test":
        print("Using test environment")
        return ".env.test"
    
    print("Using dev environment")
    return ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding="utf-8",
        extra="allow",
    )

    APP_ENV: str = "dev"
    
    DB_DRIVER: str = "postgresql"
    DB_LIBRARY: str = "psycopg"

    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    API_PREFIX: str = "/api"
    API_VERSION: str = "0.0.1"
    CORS_ORIGINS: list[str] = ["*"]

    MP12_DB_USER: str = "joao"
    MP12_DB_PASSWORD: str = ""
    MP12_DB_HOST: str = "localhost"
    MP12_DB_PORT: int = 1433
    MP12_DB_NAME: str = "MP12"

    @property
    def MP12_DB_URL(self) -> str:
        return (
            f"mssql+pyodbc://{self.MP12_DB_USER}:{self.MP12_DB_PASSWORD}"
            f"@{self.MP12_DB_HOST}:{self.MP12_DB_PORT}/{self.MP12_DB_NAME}"
            "?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        )

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_URL_WITH_LIBRARY(self) -> str:
        return f"{self.DB_DRIVER}+{self.DB_LIBRARY}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
