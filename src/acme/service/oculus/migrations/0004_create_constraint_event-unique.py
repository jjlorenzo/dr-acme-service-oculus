# Generated by Django 4.0.1 on 2022-01-19 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oculus', '0003_create_model_result_error'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('name', 'payload', 'category', 'session', 'timestamp'), name='event-unique'),
        ),
    ]