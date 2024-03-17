from typing import Optional

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser

from poll.models import Choice


class CustomUser(AbstractUser):
	# Choices will contain all choices that were picked by the user
	choices = models.ManyToManyField(
		Choice,
		related_name='users'
	)

	def get_selected_choice(self, queryset: QuerySet) -> Optional[Choice]:
		"""
		Returns a choice, if it was found in a queryset; 
		otherwise returns None or raises the exception,
		because user can have only one selected choice in a queryset
		"""
		selected_choice = self.choices.filter(id__in=queryset.values('id')).first()
		return selected_choice

	def remove_choice(self, choice: Choice) -> None:
		"""Removes choice from the 'choices'"""
		self.choices.remove(choice)

	def add_choice(self, choice: Choice) -> None:
		"""Adds choice from the 'choices'"""
		self.choices.add(choice)
