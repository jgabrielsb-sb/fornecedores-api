from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

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

    @property
    def DB_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DB_URL_WITH_LIBRARY(self) -> str:
        return f"{self.DB_DRIVER}+{self.DB_LIBRARY}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
