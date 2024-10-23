from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str
    app_description: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str
    first_superuser_email: EmailStr
    first_superuser_password: str

    class Config:
        env_file = '.env'


settings = Settings()
