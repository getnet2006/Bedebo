from pydantic_settings import BaseSettings as PydanticBaseSettings

# For Pydantic V2 (recommended)
class Settings(PydanticBaseSettings):
    APP_NAME: str = "Bedebo API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    DATABASE_URL: str 
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }
settings = Settings()
