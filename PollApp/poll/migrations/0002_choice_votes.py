# Generated by Django 5.0.1 on 2024-01-24 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
