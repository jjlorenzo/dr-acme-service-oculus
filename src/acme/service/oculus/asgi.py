import django.core.asgi
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "acme.service.oculus.conf")

application = django.core.asgi.get_asgi_application()
