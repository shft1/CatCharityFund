from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    env_app_title: str = 'QRKot'
    env_app_description: str = 'Вместе мы спасем мохнатых друзей!'
    env_database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    env_secret: str = 'bananas'
    env_first_superuser_email: EmailStr = 'root@admin.ru'
    env_first_superuser_password: str = 'root'

    class Config:
        env_file = '.env'


settings = Settings()
