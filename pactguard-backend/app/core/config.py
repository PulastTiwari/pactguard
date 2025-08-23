from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str = "sk-your-key-here"
    
    # Portia Configuration
    portia_api_key: str = "prt-your-key-here"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # API Security
    api_key: str = "dev_key"
    
    # Application Settings
    log_level: str = "INFO"
    debug: bool = True
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance  
settings = Settings()
