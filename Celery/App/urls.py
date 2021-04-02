from django.urls import path
from .views import EmailVerificationView, EmailSentView

app_name = "Email"

urlpatterns = [
	path('verify/', EmailVerificationView.as_view(), name='emailverification'),
	path('emailsent/', EmailSentView.as_view(), name='emailsent'),
]
