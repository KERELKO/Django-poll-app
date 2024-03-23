from django.db import models
from django.conf import settings


class Poll(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    votes = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_result(self) -> dict['Choice', float]:
        """
        Computes the result of the poll as a percentage for each choice.

        This method calculates the result of the poll using a simple mathematical
        formula: votes for each choice divided by the total votes in the poll,
        multiplied by 100. The result is rounded to two decimal places.

        Returns:
            A dictionary where the keys are the choice instances and the values
            are the percentage of votes each choice received.
        """
        result = {}
        choices = self.choices.all()
        for choice in choices:
            if not choice.votes or not self.votes:
                result[choice] = 0
            else:
                result[choice] = round((choice.votes / self.votes) * 100, 2)
        return result

    def increase_votes(self):
        """Increases 'votes' by 1"""
        self.votes += 1
        self.save()

    def decrease_votes(self):
        """Decreases 'votes' by 1"""
        self.votes -= 1
        self.save()

    def update_vote(
        self,
        user: 'CustomUser',
        selected_choice: int,
    ) -> None:
        """
        Updates user's vote for the poll
        """
        choices = self.choices.all()
        user_choice = user.get_selected_choice(choices)
        if user_choice:
            # remove previous vote of the user
            user_choice.decrease_votes()
            user.remove_choice(user_choice)
        elif not user_choice:
            self.increase_votes()
        # update values
        user.add_choice(selected_choice)
        selected_choice.increase_votes()


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='choices'
    )
    choice = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice

    def increase_votes(self) -> None:
        """increases 'votes' by 1"""
        self.votes += 1
        self.save()

    def decrease_votes(self) -> None:
        """decreases 'votes' by 1"""
        self.votes -= 1
        self.save()
