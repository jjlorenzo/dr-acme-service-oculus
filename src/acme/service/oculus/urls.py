import django.urls
from .api import analytics
from .api import ingress

urlpatterns = [
  django.urls.path("analytics/api/", django.urls.include((analytics.urls, "oculus"), namespace="analytics")),
  django.urls.path("ingress/api/", django.urls.include((ingress.urls, "oculus"), namespace="ingress")),
]
