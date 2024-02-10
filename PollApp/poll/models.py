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
		if not queryset:
			queryset = self.choices.all()
		total = 0
		for choice in queryset:
			total += choice.votes
		return total 


class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE,
							 	   related_name='choices')
	user_votes = models.ManyToManyField(User, related_name='voted_for')
	choice = models.CharField(max_length=200)
	votes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.choice
