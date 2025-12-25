from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Crowdfunding API"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
