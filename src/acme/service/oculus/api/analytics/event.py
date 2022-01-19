from ... import models
from rest_framework import response
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets


class ViewSet(viewsets.ViewSet):

  def list(self, request):
    filters = {}
    ordering = []
    if category := request.query_params.get("category"):
      filters["category"] = serializers.CharField().to_internal_value(category)
    if session := request.query_params.get("session"):
      filters["session"] = serializers.CharField().to_internal_value(session)
      ordering.append("timestamp")
    if timestamp_after := request.query_params.get("timestamp-after"):
      filters["timestamp__gte"] = serializers.DateTimeField().to_internal_value(timestamp_after)
    if timestamp_before := request.query_params.get("timestamp-before"):
      filters["timestamp__lte"] = serializers.DateTimeField().to_internal_value(timestamp_before)
    queryset = models.Event.objects.filter(**filters).order_by(*ordering)

    serializer = ListSerializer(
      queryset,
      many=True,
      context={},
    )
    return response.Response(serializer.data, status=status.HTTP_200_OK)


class ListSerializer(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()
  payload = serializers.JSONField()
  category = serializers.CharField()
  session = serializers.CharField()
  timestamp = serializers.DateTimeField()
