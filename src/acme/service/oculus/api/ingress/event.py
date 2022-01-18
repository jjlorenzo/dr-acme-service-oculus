import celery
import django.utils.timezone
import traceback
from ... import models
from datetime import datetime
from rest_framework import response
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets


class ViewSet(viewsets.ViewSet):
  """
  ViewSet for `Event` ingress, mounted at `/ingress/api/events`.
  """

  def create(self, request):
    """
    This endpoint should receive almost all traffic, so it doesn't process events at realtime, instead:

      - enqueue data using the distributed task queue (Celery)
      - acknowledge the reception of data
    """
    create.apply_async(
      kwargs={
        "auth": request.META.get("HTTP_AUTHORIZATION", ""),
        "received_at": django.utils.timezone.now().isoformat(),
        "data": request.data,
      },
    )
    return response.Response(status=status.HTTP_202_ACCEPTED)


@celery.shared_task
def create(*, auth: str, received_at: str, data):
  """
  Process previously enqueued Event data, creating the `Event` record or the `ResultError` with details for further
  inspection.
  """
  serializer = CreateSerializer(
    context={
      "auth": auth,
      "received_at": datetime.fromisoformat(received_at),
    },
    data=data,
  )
  try:
    serializer.is_valid(raise_exception=True)
    serializer.save()
  except Exception as exc:
    models.ResultError.objects.create(
      source=models.ResultError.SOURCE_EVENT,
      auth=auth,
      received_at=received_at,
      request=data,
      response="{exc}\n\n{tcb}".format(
        exc=exc,
        tcb="".join(traceback.format_tb(exc.__traceback__))
      ),
    )


class CreateSerializer(serializers.Serializer):
  """
  Serializer in charge of validating the received data and persisting the Event record.

  Remarks:
  We use the simpler `Serializer` instead of `ModelSerializer` because we don't need the magic and complexity
  from the later.
  """
  name = serializers.CharField(max_length=15)
  data = serializers.JSONField()  # type:ignore
  category = serializers.CharField(max_length=20)
  session_id = serializers.CharField(max_length=50)
  timestamp = serializers.DateTimeField()

  def validate_payload(self, *, payload, category, name, **kwargs):
    """
    Specific payload validations.

    Remarks:
    Current validation rules are quite simpler, basically only checks the presence of the props from the example.
    Another alternative is to use `jsonschema` since it allows to check not only the presence of props but also the
    type of values. 
    """
    errors = {}
    match category:
      case "form interaction":
        match name:
          case "submit":
            if missing := {"host", "path", "form"} - payload.keys():
              errors = {"required props": ", ".join(missing)}
      case "page interaction":
        match name:
          case "cta click":
            if missing := {"host", "path", "element"} - payload.keys():
              errors = {"required props": ", ".join(missing)}
          case "pageview":
            if missing := {"host", "path"} - payload.keys():
              errors = {"required props": ", ".join(missing)}
    if errors:
      raise serializers.ValidationError(errors)

  def validate_timestamp(self, value):
    """
    Ensure event timestamp occurs before the event was received.
    """
    if self.context["received_at"] < value:
      raise serializers.ValidationError("'timestamp' greater than 'received_at'")
    return value

  def validate(self, validate_data):
    """
    Final validation stage:

      - checks auth credentials
      - rename received data props:
          - data to payload
          - session_id to session
      - apply specifics payload validation, depending on category and name
    """
    try:
      models.Application.authenticate(apikey=self.context["auth"])
    except Exception:
      raise serializers.ValidationError("Invalid auth credentials")
    validate_data["payload"] = validate_data.pop("data")
    validate_data["session"] = validate_data.pop("session_id")
    self.validate_payload(**validate_data)
    return validate_data

  def create(self, validate_data):
    return models.Event.objects.create(**validate_data)
