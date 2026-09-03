from celery import Celery
from backend.src.config.mail import FastMailProvider
from pydantic import EmailStr
import aiosmtplib
from backend.src.config.config_env import redis_url
import asyncio
import logging
celery_app = Celery(
    broker=redis_url,
    backend=redis_url 
)
logger = logging.getLogger(__name__)
celery_app.config_from_object("backend.src.config.config_env")

@celery_app.task(autoretry_for=(aiosmtplib.SMTPException,ConnectionError),retry_backoff=True,retry_kwargs={"max_retries":5})
def email_task_queue(subject:str,email:str,body:str):
    try:
      mail_provider = FastMailProvider()
      asyncio.run(mail_provider.create_email(email,subject,body))
      logger.info(f"[EMAIL TASK] E-mail enviado com sucesso para: {email}")
    except Exception as exc:
        logger.error(f"[EMAIL TASK ERRO] Falha no envio: {exc}", exc_info=True)
        raise exc