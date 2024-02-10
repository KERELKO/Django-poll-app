from django import forms
from .models import Choice, Poll


class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice']
		

class PollForm(forms.ModelForm):
	class Meta:
		model = Poll 
		fields = '__all__'
		exclude = ['created', 'owner']
