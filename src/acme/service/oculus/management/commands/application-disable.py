import django.core.management.base
import json
import sys
import uuid
from ... import models


class Command(django.core.management.base.BaseCommand):
  """
  Used for disabling access to an existing Application (client)
  ``` sh
  $ poetry run django-admin application-disable e5490d29-f9d6-425c-b74e-38ae9f145b21
  {
    "id": "e5490d29-f9d6-425c-b74e-38ae9f145b21",
    "name": "app2",
    "apikey": "eyJjcmMDAifQ...UbC3qekEMSLw",
    "active": false
  }
  ```
  """

  help = ""

  def add_arguments(self, parser: django.core.management.base.CommandParser):
    """"""
    parser.add_argument("id", type=uuid.UUID)

  def handle(self, id, **options):
    """"""
    try:
      application = models.Application.disable(id=id)
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
