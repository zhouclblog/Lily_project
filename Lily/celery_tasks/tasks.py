from celery import Celery
from django.core.mail import send_mail
from Lily.settings import EMAIL_HOST_USER

app = Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/3")

@app.task
def send_active_email(token, email, username):

	subject = "Lily服装商城用户激活"
	message = ""
	from_email = EMAIL_HOST_USER
	recipient_list = [email]
	html_message = "<a href='http://127.0.0.1:8000/user/active?token=%s'>href='http://127.0.0.1:8000/user/active/</a>" % token

	send_mail(subject, message, from_email, recipient_list, html_message=html_message)

