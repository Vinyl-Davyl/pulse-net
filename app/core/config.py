from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./test.db"
    jwt_secret: str
    jwt_lifetime_seconds: int = 3600
    imagekit_private_key: str
    imagekit_public_key: str
    imagekit_url_endpoint: str = Field(validation_alias="IMAGEKIT_URL")


settings = Settings()
