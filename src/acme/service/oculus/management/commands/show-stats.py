import django.core.management.base
import json
import sys
from ... import models


class Command(django.core.management.base.BaseCommand):

  help = "Show stats for 'acme.service.oculus'"

  def add_arguments(self, parser: django.core.management.base.CommandParser):
    pass

  def handle(self, *args, **options):
    applications = models.Application.objects.all()
    response = {
      "application": {
        "count": applications.count(),
        "items": [{
          "id": str(application.id),
          "name": application.name,
          "apikey": application.apikey,
          "active": application.active,
        } for application in applications],
      },
    }
    self.stdout.write(json.dumps(response, indent=2))
    sys.exit(0)
