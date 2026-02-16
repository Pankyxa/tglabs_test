from sqlalchemy.ext.asyncio import AsyncEngine
from langchain_community.utilities import SQLDatabase
from src.settings import settings
from src.db import engine as main_engine


def get_async_engine() -> AsyncEngine:
    return main_engine


def get_schema_info() -> str:
    """
    LangChain требует СИНХРОННОГО драйвера (psycopg2) для анализа схемы
    Поэтому мы временно создаем синхронный URL
    """
    sync_db_uri = (
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}@{settings.postgres_host}:"
        f"{settings.postgres_port}/{settings.postgres_database}"
    )

    try:
        db = SQLDatabase.from_uri(sync_db_uri)
        return db.get_table_info()
    except Exception as e:
        print(f"Warning: Could not fetch table schema: {e}")
        return ""