from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Вместе мы спасем мохнатых друзей!'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'bananas'
    first_superuser_email: EmailStr = 'root@admin.ru'
    first_superuser_password: str = 'root'

    class Config:
        env_file = '.env'


settings = Settings()
