import os
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings



# -----------------------------
# Settings for FastAPI Backend
# -----------------------------
# All sensitive values should be set in a .env file (never hardcoded here).
# Example .env:
# APP_NAME=MyApp
# APP_VERSION=1.0.0
# DEBUG=True
# SECRET_KEY=your-secret-key
# BASE_URL=http://localhost:8000
# POSTGRES_USER=postgres
# POSTGRES_PASSWORD=yourpassword
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432
# POSTGRES_DB=yourdb
# CORS_ORIGINS=["http://localhost:5173"]
# OPENAI_API_KEY=your-openai-key
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASS=your-email-password
# IMAP_SERVER=imap.gmail.com
# IMAP_PORT=993
# IMAP_USER=your-email@gmail.com
# IMAP_PASS=your-email-password

class Settings(BaseSettings):
    # General app settings
    app_name: str = Field(default="FastAPI Application", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    secret_key: str = Field(default="changeme", env="SECRET_KEY")  # Set in .env for production
    base_url: str = Field(default="http://localhost:8000", env="BASE_URL")

    # Database settings
    postgres_user: str = Field(default="postgres", env="POSTGRES_USER")
    postgres_password: str = Field(default="root", env="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_db: str = Field(default="hrms_dev", env="POSTGRES_DB")

    # CORS settings (restrict for dev, set properly for prod)
    cors_origins: List[str] = Field(default=["http://localhost:5173"], env="CORS_ORIGINS")

    # Third-party API keys (never commit real keys)
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")

    # SMTP server settings
    smtp_host: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: str = Field(default="", env="SMTP_USER")
    smtp_password: str = Field(default="", env="SMTP_PASS")

    # IMAP server settings
    imap_server: str = Field(default="imap.gmail.com", env="IMAP_SERVER")
    imap_port: int = Field(default=993, env="IMAP_PORT")
    imap_username: str = Field(default="", env="IMAP_USER")
    imap_password: str = Field(default="", env="IMAP_PASS")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def database_url_sync(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
