from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_DOOR:int
    ADM_PASSWORD:str
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM:str
    MAIL_FROM_NAME:str
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
mail_username = env.MAIL_USERNAME
mail_password = env.MAIL_PASSWORD
mail_port = env.MAIL_PORT
mail_server = env.MAIL_SERVER
mail_from = env.MAIL_FROM
mail_from_name = env.MAIL_FROM_NAME