from rest_framework import response
from rest_framework import status
from rest_framework import viewsets


class ViewSet(viewsets.ViewSet):

  def list(self, request):
    return response.Response([], status=status.HTTP_200_OK)
