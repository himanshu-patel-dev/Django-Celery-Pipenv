from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import send_email

logger = get_task_logger(__name__)

@task(name="sending email")
def send_email_task(name, email):
	logger.info("Sent verification email")
	send_email(name, email)

@shared_task
def add(x,y):
	return x+y
