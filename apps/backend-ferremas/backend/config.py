from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """App settings."""
    database_url: str = "sqlite:///./db.sqlite3"


settings = Settings()
