import django.core.management.base
import json
import sys
from ... import models


class Command(django.core.management.base.BaseCommand):

  help = ""

  def add_arguments(self, parser: django.core.management.base.CommandParser):
    parser.add_argument("name", type=str)

  def handle(self, name, **options):
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
