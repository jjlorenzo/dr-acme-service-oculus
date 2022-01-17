from django.db import models


class Event(models.Model):
  name = models.CharField(max_length=15)
  payload = models.JSONField()
  category = models.CharField(max_length=20)
  session = models.CharField(max_length=50)
  timestamp = models.DateTimeField()
