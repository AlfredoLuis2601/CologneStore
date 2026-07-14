from celery import Celery
from src.config.mail import FastMailProvider
from pydantic import EmailStr
import smtplib
from src.config.config_env import redis_url
import asyncio

celery_app = Celery(
    broker=redis_url,
    backend=redis_url 
)

celery_app.config_from_object("src.config.config_env")
#Celery doesn't support async functionality
@celery_app.task(autoretry_for=(smtplib.SMTPException,ConnectionError),retry_backoff=True,retry_kwargs={"max_retries":5})
def email_task_queue(subject:str,email:EmailStr,body:str):
    mail_provider = FastMailProvider()
    asyncio.run(mail_provider.create_email(email,subject,body))