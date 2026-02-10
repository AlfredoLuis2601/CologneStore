from celery import Celery
from .mail import Email,creating_email,mail_setup
from .config_env import redis_url
import asyncio
celery_app = Celery(
    broker=redis_url,
    backend=redis_url 
)

celery_app.config_from_object("cologne.config_env")
#Celery doesn't support async functionality
@celery_app.task()
def email_task_queue(subject:str,email:Email,body:str):
    message = creating_email(email=email,subject=subject,body=body)
    asyncio.run(mail_setup.send_message(message=message))