from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .forms import EmailVerificationForm
from django.views.generic.edit import FormView


class EmailSentView(TemplateView):
	template_name = "App/EmailSent.html"


class EmailVerificationView(FormView):
	template_name = "App/VerifyEmail.html"
	form_class = EmailVerificationForm
 
	def form_valid(self, form):
		form.send_email()
		return redirect('Email:emailsent')
