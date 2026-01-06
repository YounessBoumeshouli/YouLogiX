from pydantic_settings import BaseSettings
# Settings class
class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        case_sensitive = False
settings = Settings()