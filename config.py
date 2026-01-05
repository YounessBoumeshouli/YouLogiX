from pydantic_settings import BaseSettings
# Settings class
class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    class Config:
        env_file = ".env"  # Load from .env automatically
        extra = "ignore"   #ignore extra variables
        case_sensitive = False #not senstive with uppercases
settings = Settings()