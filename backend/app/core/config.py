from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = "/home/lamka/Desktop/MyProjects/Projects/Personalizo.al/backend/.env"

settings = Settings()
print("✅ ENV LOADED:", settings.SECRET_KEY)
