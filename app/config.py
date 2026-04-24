from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_EMAIL: str = "admin@policyconsultant.com"
    ADMIN_PASSWORD: str = "Admin@12345"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://policy-consultant.vercel.app,https://policy-consultant-git-main-shivani-gulhanes-projects.vercel.app"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
