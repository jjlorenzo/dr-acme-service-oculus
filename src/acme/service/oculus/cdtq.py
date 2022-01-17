import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.service.oculus.conf")

application = celery.Celery("oculus")

application.config_from_object("django.conf:settings", namespace="CELERY")
