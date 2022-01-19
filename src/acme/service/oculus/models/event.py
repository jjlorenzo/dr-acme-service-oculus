from django.db import models


class Event(models.Model):
  """
  An event **received** by the api and **processed** by the distributed task queue
  """

  name = models.CharField(max_length=15)
  payload = models.JSONField()
  category = models.CharField(max_length=20)
  session = models.CharField(max_length=50)
  timestamp = models.DateTimeField()

  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=[
          "name",
          "payload",
          "category",
          "session",
          "timestamp",
        ],
        name="event-unique",
      ),
    ]
