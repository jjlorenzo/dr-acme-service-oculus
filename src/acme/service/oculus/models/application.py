import django.core.signing
import django.utils.timezone
import typing
import uuid
from django.db import models


def get_decrypted_apikey(*, apikey, salt="apikey.application.oculus.service.acme"):
  obj = django.core.signing.loads(apikey, salt=salt)
  return obj


def get_encrypted_apikey(*, salt="apikey.application.oculus.service.acme"):
  obj = {
    "created_at": django.utils.timezone.now().isoformat(),
  }
  return django.core.signing.dumps(obj, salt=salt)


class Application(models.Model):

  id = models.UUIDField(default=uuid.uuid4, primary_key=True)
  name = models.CharField(max_length=100, unique=True)
  apikey = models.CharField(default=get_encrypted_apikey, max_length=200, unique=True)
  active = models.BooleanField(default=True)

  @classmethod
  def authenticate(cls, *, apikey: str) -> typing.Union["Application", None]:
    """
    """
    if apikey.startswith("ApiKey "):
      apikey = apikey[7:]
    get_decrypted_apikey(apikey=apikey)
    obj = cls.objects.get(apikey=apikey, active=True)
    return obj

  @classmethod
  def create(cls, *, name: str) -> "Application":
    """
    """
    obj = cls.objects.create(name=name)
    return obj

  @classmethod
  def disable(cls, *, id: uuid.UUID) -> "Application":
    """
    """
    obj = cls.objects.get(id=id)
    obj.active = False
    obj.save(update_fields=["active"])
    return obj
