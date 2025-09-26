from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_collection: str = "leads_collection"