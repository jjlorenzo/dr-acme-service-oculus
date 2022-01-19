import celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.service.oculus.conf")

application = celery.Celery(
  broker="amqp://guest:guest@localhost//",
  main="oculus",
)
