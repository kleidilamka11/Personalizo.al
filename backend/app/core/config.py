from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    REDIS_URL: str = "redis://localhost:6379/0"

    BASE_URL: str = "http://localhost:8000"

    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM: str = "no-reply@example.com"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
print("SMTP_HOST loaded as:", settings.SMTP_HOST)
print("REDIS_URL loaded as:", settings.REDIS_URL)
