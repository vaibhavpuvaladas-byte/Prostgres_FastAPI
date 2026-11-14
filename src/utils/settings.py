from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    DB_CONNECTION : str
    secret_key : str
    algorithm : str
    EXP_TIME_MINUTES : int

settings = Settings()

