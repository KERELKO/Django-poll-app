from django.contrib import admin
from .models import Poll, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
	list_display = ['owner', 'title', 'description']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	list_display = ['choice', 'poll', 'votes']
