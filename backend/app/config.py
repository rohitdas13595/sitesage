from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from functools import lru_cache
from typing import List, Union, Any


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Database
    DATABASE_URL: str = "postgresql://sitesage:sitesage@db:5432/sitesage"
    
    # Google Gemini API
    GOOGLE_API_KEY: str = ""
    LLM_MODEL: str = "gemini-1.5-flash"
    
    # Application
    APP_NAME: str = "SiteSage"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Auth
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = "*"
    
    # AWS S3 (optional)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_BUCKET_NAME: str = ""
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> Union[str, List[str]]:
        if isinstance(v, str) and v != "*":
            return [origin.strip() for origin in v.split(',')]
        if not v:
            return "*"
        return v
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
