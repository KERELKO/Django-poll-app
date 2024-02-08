from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=400, blank=False)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.description

	def get_result(self) -> dict:
		"""
		count result of the poll using,
		simple math formula, before this takes all
		votes of the choices and compute their sum
		"""
		result = {}
		choices = self.choices.all()
		total_votes = sum([choice.votes for choice in choices])
		for choice in choices:
			if choice.votes == 0:
				result[choice.id] = 0
				continue
			result[choice.id] = round((choice.votes / total_votes) * 100, 2)
		return result


class Choice(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE,
							 	   related_name='choices')
	choice = models.CharField(max_length=200)
	user_votes = models.ManyToManyField(User, 
										related_name='voted_choices')
	votes = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.choice

