from celery import Celery
from src.mail_support.mail import Email,creating_email,mail_setup
from src.config.config_env import redis_url
import asyncio
celery_app = Celery(
    broker=redis_url,
    backend=redis_url 
)

celery_app.config_from_object("src.config.config_env")
#Celery doesn't support async functionality
@celery_app.task()
def email_task_queue(subject:str,email:Email,body:str):
    message = creating_email(email=email,subject=subject,body=body)
    asyncio.run(mail_setup.send_message(message=message))