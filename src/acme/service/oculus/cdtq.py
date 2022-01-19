import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.service.oculus.conf")

application = celery.Celery(
  broker=os.environ.get("OCULUS_BROKER", "amqp://guest:guest@localhost//"),
  main="oculus",
)
