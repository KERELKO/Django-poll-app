from typing import Type, Optional

from django.views.generic.detail import DetailView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count

from .models import Poll, Choice
from .mixins import OwnerEditMixin


class PollListView(ListView):
	queryset = Poll.objects.annotate(
		num_choices=Count('choices')
	).order_by('-created')
	template_name = 'polls/list.html'


class PollCreateView(LoginRequiredMixin, CreateView):
	model = Poll
	template_name = 'polls/create.html'
	fields = ['title', 'description']

	def get_success_url(self):
		success_url = reverse_lazy(
			'poll:detail', 
			kwargs={'pk': self.object.id}
		)
		return success_url

	def form_valid(self, form):
		form.instance.owner = self.request.user 
		response = super().form_valid(form)
		for i in range(5):	
			choice = f'content-{i}'
			if choice in self.request.POST:
				Choice.objects.create(
					poll=self.object, 
					choice=self.request.POST[choice]
				)	
		return response 


class PollEditView(OwnerEditMixin, UpdateView):
	model = Poll
	template_name = 'polls/edit.html'
	context_object_name = 'poll'
	fields = ['title', 'description']
	
	def get_success_url(self):
		success_url = reverse_lazy(
			'poll:detail', 
			kwargs={'pk': self.pk}
		)
		return success_url


class PollDetailView(LoginRequiredMixin, DetailView):
	model = Poll  
	context_object_name = 'poll'
	template_name = 'polls/detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['choices'] = {}
		poll = self.object
		choices = poll.choices.all()
		user_choice = self.request.user.get_selected_choice(choices)
		if user_choice:
			context['selected_choice_id'] = user_choice.id
		context['choices'] = {choice.id: choice.choice for choice in choices}
		return context

	def post(self, request, pk): 
		poll = get_object_or_404(Poll, id=pk)
		choice_id = int(request.POST.get('choices'))
		selected_choice = get_object_or_404(Choice, id=choice_id)
		
		# update fields
		poll.update_vote(selected_choice=selected_choice, user=request.user)

		# message
		messages.success(request, 'Vote counted!')
		return redirect('poll:detail', pk=pk)


class PollResultView(TemplateResponseMixin, View):
	template_name = 'polls/result.html'

	def get_selected_choice(
		self, 
		user: Type['User'], 
		queryset: Type['queryset']
	) -> Optional[Type['Choice']]:
		selected_choice = user.get_selected_choice(queryset)
		if not selected_choice:
			return None
		return selected_choice

	def get(self, request, pk):
		context = {}
		poll = get_object_or_404(Poll, id=pk)
		choices = poll.choices.all()
		poll_result = poll.get_result()
		selected_choice = self.get_selected_choice(request.user, choices)
		if selected_choice:
			context['selected_choice_id']: selected_choice.id
		context_choices = {}
		for choice in choices:
			context_choices[choice.id] = [
				choice.choice, 
				poll_result[choice.id]
			]
		context = {
			'choices': context_choices,
			'poll': poll,
		}
		return self.render_to_response(context)


class PollDeleteView(OwnerEditMixin, View):
	model = Poll

	def dispatch(self, request, pk, *args, **kwargs):
		super().dispatch(request, pk, *args, **kwargs)
		return self.delete(request, pk)

	def delete(self, request, pk):
		poll = get_object_or_404(Poll, id=pk)
		poll.delete()
		return redirect('poll:list')
