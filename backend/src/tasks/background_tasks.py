from celery import Celery
from pydantic import EmailStr
import resend
from backend.src.config.config_env import redis_url,resend_api_key
import asyncio
import logging
celery_app = Celery(
    broker=redis_url,
    backend=redis_url 
)
resend.api_key = resend_api_key
logger = logging.getLogger(__name__)
celery_app.config_from_object("backend.src.config.config_env")

@celery_app.task(autoretry_for=(ConnectionError,Exception),retry_backoff=True,retry_kwargs={"max_retries":5})
def email_task_queue(subject:str,email:str,body:str):
    try:
      params: resend.Emails.SendParams ={
          "from": "Cologne Store <onboarding@resend.dev>",
          "to": [email],
          "subject": subject,
          "html": body
      }
      response = resend.Emails.send(params)
      logger.info(f"[EMAIL TASK] E-mail enviado com sucesso para: {email}, ID: {response.get("id")}")
    except Exception as exc:
        logger.error(f"[EMAIL TASK ERRO] Falha no envio: {exc}", exc_info=True)
        raise exc