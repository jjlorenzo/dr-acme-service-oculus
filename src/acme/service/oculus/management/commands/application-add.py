import django.core.management.base
import json
import sys
from ... import models


class Command(django.core.management.base.BaseCommand):
  """
  Used for creating credentials for a new Application (client)
  ```
  $ poetry run django-admin application-add app-1
  {
    "id": "e5490d29-f9d6-425c-b74e-38ae9f145b21",
    "name": "app-1",
    "apikey": "eyJjcmMDAifQ...UbC3qekEMSLw",
    "active": true
  }
  ```
  """

  help = ""

  def add_arguments(self, parser: django.core.management.base.CommandParser):
    """"""
    parser.add_argument("name", type=str)

  def handle(self, name, **options):
    """"""
    try:
      application = models.Application.create(name=name)
    except Exception as exc:
      response = {
        "err": type(exc).__name__,
        "msg": str(exc).strip(),
      }
      self.stderr.write(json.dumps(response, indent=2))
      sys.exit(1)
    else:
      response = {
        "id": str(application.id),
        "name": application.name,
        "apikey": application.apikey,
        "active": application.active,
      }
      self.stdout.write(json.dumps(response, indent=2))
      sys.exit(0)
