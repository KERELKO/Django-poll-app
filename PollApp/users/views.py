from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from .forms import RegistrationForm


class UserLoginView(LoginView):
	template_name = 'users/login.html'


class UserLogout(LoginRequiredMixin, View):
    
    def get(self, request):
        logout(request)
        return redirect('poll:list')


class UserRegistrationView(View, TemplateResponseMixin):
	template_name = 'users/registration.html'

	def get(self, request):
		form = RegistrationForm()
		return self.render_to_response({'form': form})

	def post(self, request):
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			login(request, user)
			return redirect('poll:list')
		return self.render_to_response({'form': form})
