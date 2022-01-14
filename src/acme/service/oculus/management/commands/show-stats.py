import django.core.management.base


class Command(django.core.management.base.BaseCommand):

  help = "Show stats for 'acme.service.oculus'"

  def add_arguments(self, parser: django.core.management.base.CommandParser):
    pass

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS("✔ OK"))
