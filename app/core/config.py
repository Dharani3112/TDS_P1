import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
      # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # AI Pipe Configuration
    aipipe_token: Optional[str] = None
    aipipe_base_url: str = "https://aipipe.org/api/v1"
    
    # OpenAI Configuration (Legacy - now using AI Pipe)
    openai_api_key: Optional[str] = None
    default_model: str = "gpt-4o-mini"
    max_tokens: int = 1000
    temperature: float = 0.1
    
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "tds_virtual_ta"
    
    # Scraping Configuration
    course_url: str = "https://tds.s-anand.net/"
    discourse_url: str = "https://discourse.onlinedegree.iitm.ac.in/"
    max_pages_per_site: int = 100
    request_delay: float = 1.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
