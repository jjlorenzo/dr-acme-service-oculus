import django.core.management.base
import json
import sys
from ... import models


class Command(django.core.management.base.BaseCommand):
  """
  Show stats for service data
  ``` sh
  $ poetry run django-admin show-stats
  {
    "application": {
      "count": 2,
      "items": [
        {
          "id": "7a6d47fa-00e3-49fd-a6bf-bca002d50db9",
          "name": "app",
          "apikey": "eyJjcmVhdGVk...vlM2Sc0XJDsM",
          "active": true
        },
        {
          "id": "e5490d29-f9d6-425c-b74e-38ae9f145b21",
          "name": "app2",
          "apikey": "eyJjcmMDAifQ...UbC3qekEMSLw",
          "active": false
        }
      ]
    },
    "events": {
      "count": 19,
      "latest": [
        {
          "id": 11,
          "name": "pageview",
          "payload": {
            "host": "www.consumeraffairs.com",
            "path": "/"
          },
          "category": "page interaction",
          "session": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
          "timestamp": "2021-01-01T09:15:27.243860+00:00"
        }
      ]
    }
  }
  ```
  """

  help = ""

  def handle(self, *args, **options):
    """"""
    applications = models.Application.objects.all()
    events = models.Event.objects.all()
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
      "events": {
        "count": events.count(),
        "latest": [{
          "id": event.id,
          "name": event.name,
          "payload": event.payload,
          "category": event.category,
          "session": event.session,
          "timestamp": event.timestamp.isoformat(),
        } for event in events[:1]],
      },
    }
    self.stdout.write(json.dumps(response, indent=2))
    sys.exit(0)
