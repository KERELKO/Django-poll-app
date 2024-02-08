from django import forms
from django.contrib.auth.models import User 
from .models import Choice, Poll


class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User 
		fields = ['username', 'first_name', 'last_name', 'email']

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Passwords don\'t match.')
		return cd['password2']


class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice']
		

class PollForm(forms.ModelForm):
	class Meta:
		model = Poll 
		fields = ['description']
