from typing import Union, Type
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import MultipleObjectsReturned

from poll.models import Choice


class CustomUser(AbstractUser):
	choices = models.ManyToManyField(
		Choice,
		related_name='users'
	)

	def get_selected_choice(self, queryset: QuerySet) -> Union[Type['Choice'], None]:
		"""
		Returns a choice, if it was found in a queryset; 
		otherwise returns None or raises the exception,
		because user can have only one selected choice in a queryset
		"""
		selected_choices = self.choices.filter(choice__in=queryset)
		if len(selected_choices) >= 2:
			raise MultipleObjectsReturned('User cannot have two or more selected choices in a queryset')
		if len(selected_choices) == 1:
			return selected_choices.first()
		return None

	def remove_choice(self, choice: Type['Choice']) -> None:
		"""Removes choice from the 'choices'"""
		self.choices.remove(choice)

	def add_choice(self, choice: Type['Choice']) -> None:
		"""Adds choice from the 'choices'"""
		self.choices.add(choice)
