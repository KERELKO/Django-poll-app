from typing import Type  
from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
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
		total = 0
		if not queryset:
			queryset = self.choices.all()
		for choice in queryset:
			total += choice.votes
		return total 

	def change_vote(self,  
		selected_choice: Type['Choice'],
		user: Type['User']
	) -> None:
		"""
		Change user's vote for the poll, 
		using 'add_user' and 'remove_user' 
		methods of the Choice  
		"""
		for choice in self.choices.all():
			if choice.has_user(user) and choice.id != selected_choice.id:
				choice.remove_user(user)
				break
		if not selected_choice.has_user(user):
			selected_choice.add_user(user)


class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE,
							 	   related_name='choices')
	user_votes = models.ManyToManyField(User, related_name='voted_for')
	choice = models.CharField(max_length=200)
	votes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.choice

	def add_user(self, user: Type['User']) -> None:
		"""
		Add user to the 'user_votes' field,
		also increase votes field by 1
		"""
		self.user_votes.add(user)
		self.votes += 1
		self.save()

	def remove_user(self, user: Type['User']) -> None:
		"""
		Remove user from the 'user_votes' field,
		also decrease votes field by 1
		"""
		self.votes -= 1
		self.user_votes.remove(user)
		self.save()

	def has_user(self, user: Type['User']) -> bool:
		"""Check if the user has already voted"""
		return user in self.user_votes.all()
