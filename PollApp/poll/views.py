from django.views.generic.detail import DetailView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from .models import Poll, Choice
from .mixins import OwnerEditMixin


class PollListView(ListView):
	queryset = Poll.objects.annotate(num_choices=Count('choices')) \
						   .order_by('-created')
	template_name = 'polls/list.html'


class PollCreateView(LoginRequiredMixin, CreateView):
	model = Poll
	template_name = 'polls/create.html'
	fields = ['description']

	def get_success_url(self):
		success_url = reverse_lazy('poll:detail', 
									kwargs={'pk': self.object.id})
		return success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context
	
	def form_valid(self, form):
		form.instance.owner = self.request.user 
		response = super().form_valid(form)
		for i in range(5):	
			choice = f'content-{i}'
			if choice in self.request.POST:
				Choice.objects.create(poll=self.object, 
									  choice=self.request.POST[choice])	
		return response 


class PollEditView(OwnerEditMixin, UpdateView):
	model = Poll
	template_name = 'polls/edit.html'
	context_object_name = 'poll'
	fields = ['description']
	
	def get_success_url(self):
		success_url = reverse_lazy('poll:detail', 
									kwargs={'pk': self.object.id})
		return success_url

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		poll = self.object
		choices = poll.choices.all()
		context['choices'] = {}
		for choice in choices:
			context['choices'][f'{choice.id}'] = choice.choice
		return context

	def form_valid(self, form):
		response = super().form_valid(form)
		poll = self.object
		for choice in poll.choices.all():
			if str(choice.id) in self.request.POST:
				choice.choice = self.request.POST[f'{choice.id}']
				choice.save()
		return response


class PollDetailView(LoginRequiredMixin, DetailView):
	model = Poll  
	context_object_name = 'poll'
	template_name = 'polls/detail.html'

	def dispatch(self, request, *args, **kwargs):
		if request.method == 'POST':
			self.template_name = 'polls/detail_done.html'
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		poll = self.object
		choices = poll.choices.all()
		poll_result = poll.get_result()
		context['choices'] = {}
		for choice in choices:
			context['choices'][f'{choice.id}'] = [choice.choice, 
												  poll_result[choice.id]]
		return context

	def post(self, request, pk):
		choice = get_object_or_404(Choice, id=request.POST['choices'])
		choice.user_votes.add(request.user)
		choice.votes += 1
		choice.save()
		return self.render_to_response({})


class PollResultView(View, TemplateResponseMixin):
	template_name = 'polls/result.html'

	def get(self, request, pk):
		poll = get_object_or_404(Poll, id=pk)
		choices = poll.choices.all()
		poll_result = poll.get_result()
		context_choices = {}
		user_choice = None
		for choice in choices:
			if request.user in choice.user_votes.all():
				user_choice = str(choice.id)
			context_choices[f'{choice.id}'] = [choice.choice, 
											   poll_result[choice.id]]
		print(choices, user_choice)
		return self.render_to_response({'choices': context_choices,
										'user_choice': user_choice,
										'poll': poll})


class PollDeleteView(OwnerEditMixin, View):

	def get(self, request, pk):
		poll = get_object_or_404(Poll, id=pk)
		poll.delete()
		return redirect('poll:list')
