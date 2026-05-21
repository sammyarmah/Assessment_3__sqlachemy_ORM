from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Social_Media"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = ""

    DATABASE_URL_ASYNC: str = ""
    DATABASE_URL_SYNC: str = ""

    # pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
