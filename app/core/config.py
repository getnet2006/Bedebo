from pydantic_settings import BaseSettings as PydanticBaseSettings

# For Pydantic V2 (recommended)
class Settings(PydanticBaseSettings):
    APP_NAME: str = "Bedebo API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite+aiosqlite:///./bedebo.db"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
settings = Settings()
