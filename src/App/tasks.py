from celery import shared_task
from celery.task import task
from celery.utils.log import get_task_logger

from .email import send_email

logger = get_task_logger(__name__)

@task()
def send_email_task(name, email):
	logger.info("Sent verification email")
	return send_email(name, email)

@shared_task
def add(x,y):
	return x+y
