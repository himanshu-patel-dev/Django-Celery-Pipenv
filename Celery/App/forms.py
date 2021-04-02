from django import forms
from .tasks import send_email_task

class EmailVerificationForm(forms.Form):
	name = forms.CharField(
		label='Firstname', 
		max_length=100, 
		widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Name'}
			)
		)
	email = forms.EmailField(
		label='Email', 
		max_length=100, 
		widget=forms.TextInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}
			)
		)

	def send_email(self):
		email = self.cleaned_data['email']
		name = self.cleaned_data['name']

		send_email_task.delay(name, email)
