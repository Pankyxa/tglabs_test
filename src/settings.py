from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str

    openrouter_api_key: str
    openrouter_model: str

    telegram_token: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env')

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_database}"
        )


settings = Settings()
