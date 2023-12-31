from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)

    SERVICE_BUS_CONN_STRING: str
    DEV_IOTHUB_CONNECTION_STRING: str


# Configuration singleton to be passed around the application
# This validates and loads the environment variables set in the .env file.
settings = Settings()