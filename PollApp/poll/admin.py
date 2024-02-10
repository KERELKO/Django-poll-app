from django.contrib import admin
from .models import Poll, Choice


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
	fields = ['owner', 'title', 'description']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
	fields = ['choice', 'poll', 'votes']
