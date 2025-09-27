from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mcp_url: str = "http://localhost:8002"


settings = Settings()