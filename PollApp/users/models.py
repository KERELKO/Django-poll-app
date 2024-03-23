from typing import Optional

from django.db import models
from django.contrib.auth.models import AbstractUser

from poll.models import Choice


class CustomUser(AbstractUser):
    # Selected choices will contain all choices that were picked by the user
    selected_choices = models.ManyToManyField(Choice, related_name='users')

    def get_selected_choice(
        self, queryset: models.QuerySet
    ) -> Optional[Choice]:
        """
        Returns a selected choice, if it was found in a queryset
        """
        selected_choice = self.selected_choices.filter(
            id__in=queryset.values('id')
        ).first()
        return selected_choice

    def remove_choice(self, choice: Choice) -> None:
        """
        Removes selected choice from the 'selected_choices'
        """
        self.selected_choices.remove(choice)

    def add_choice(self, choice: Choice) -> None:
        """
        Adds selected choice to the 'selected_choices'
        """
        self.selected_choices.add(choice)
