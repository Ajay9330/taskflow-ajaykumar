from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    
    JWT_SECRET: str
    JWT_EXPIRY_HOURS: int = 24
    
    BACKEND_PORT: int = 8080
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

settings = Settings()
