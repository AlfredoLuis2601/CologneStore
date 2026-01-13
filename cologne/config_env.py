from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_DOOR:int
    ADM_PASSWORD:str
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
env = Settings()
url_database = env.DATABASE_URL
jwt_key = env.JWT_KEY
jwt_algorithm = env.JWT_ALGORITHM
redis_host = env.REDIS_HOST
redis_door = env.REDIS_DOOR
password = env.ADM_PASSWORD