from django.db import models


class ResultError(models.Model):
  """
  A result error record for further inspection
  """

  SOURCE_EVENT = 0
  SOURCE_CHOICES = [
    (SOURCE_EVENT, "event"),
  ]

  source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES)
  auth = models.CharField(max_length=210)
  received_at = models.DateTimeField()
  request = models.JSONField()
  response = models.TextField()
