from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
class Settings(BaseSettings):
    STANDARD_EXPIRE_JWT_TIME:int = 2
    STANDARD_TOKEN_EXPIRE_TIME:int = 30
    DEFAULT_TIMEDELTA:int = 3600
    DATABASE_URL:str
    JWT_KEY:str
    JWT_ALGORITHM:str
    REDIS_URL:str 
    ADM_PASSWORD:str
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM:str
    MAIL_FROM_NAME:str
    BASE_URL:str
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
env = Settings()
url_database = env.DATABASE_URL
jwt_key = env.JWT_KEY
jwt_algorithm = env.JWT_ALGORITHM
redis_url = env.REDIS_URL
password = env.ADM_PASSWORD
mail_username = env.MAIL_USERNAME
mail_password = env.MAIL_PASSWORD
mail_port = env.MAIL_PORT
mail_server = env.MAIL_SERVER
mail_from = env.MAIL_FROM
mail_from_name = env.MAIL_FROM_NAME
base_url = env.BASE_URL
standard_expire_jwt = env.STANDARD_EXPIRE_JWT_TIME
standard_token_time = env.STANDARD_TOKEN_EXPIRE_TIME
default_time_delta = env.DEFAULT_TIMEDELTA
#Posteriormente sera a url do render e depois do site.