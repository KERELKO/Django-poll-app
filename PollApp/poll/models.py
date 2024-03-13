from typing import Type  
from django.db import models
from django.db.models import Sum
from django.conf import settings 


class Poll(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.title

	def get_result(self) -> dict:
		"""
		Count result of the poll using a simple math formula.
		Before this, take all the votes from the choices
		and compute their sum.
		"""
		result = {}
		choices = self.choices.all()
		total_votes = self.total_votes(choices)
		for choice in choices:
			if not choice.votes:
				result[choice.id] = 0
				continue
			result[choice.id] = round((choice.votes / total_votes) * 100, 2)
		return result

	def total_votes(self, queryset=None) -> int:
		"""Return total count of votes for the poll"""
		if not queryset:
			queryset = self.choices.all()
		queryset = queryset.aggregate(total_votes=Sum('votes'))
		return queryset.get('total_votes', 0)

	def update_vote(self,  
		user: Type['User'],
		selected_choice: int,
	) -> None:
		""" 
		Updates user vote for the poll
		"""
		choices = self.choices.all()
		user_choice = user.get_selected_choice(choices)
		if user_choice:
			user_choice.decrease_votes()
			user.remove_choice(user_choice)	
		user.add_choice(selected_choice)
		selected_choice.increase_votes()


class Choice(models.Model):
	poll = models.ForeignKey(
		Poll, 
		on_delete=models.CASCADE,
		related_name='choices'
	)
	choice = models.CharField(max_length=200)
	votes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.choice

	def increase_votes(self) -> None:
		""" increases 'votes' by 1"""
		self.votes += 1
		self.save()

	def decrease_votes(self) -> None:
		"""decrease 'votes' by 1"""
		self.votes -= 1
		self.save()
