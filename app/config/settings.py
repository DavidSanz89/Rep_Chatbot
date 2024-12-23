from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My App"
    openai_api_key: str
    pandasai_api_key: str

    class Config:
        env_file = ".env"  # Optional: Load settings from a .env file


settings = Settings()


