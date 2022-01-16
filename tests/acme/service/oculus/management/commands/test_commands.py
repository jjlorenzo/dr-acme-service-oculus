import pytest
from . import call_command
from acme.service.oculus import models
from django.core.management.base import CommandError

pytestmark = pytest.mark.django_db(transaction=True)


class TestGood:

  def test_application_add(self, name="app"):
    # check: application DoesNotExist
    with pytest.raises(models.Application.DoesNotExist, match="Application matching query does not exist"):
      models.Application.objects.get(name=name)
    # command: application-add
    ret, out, err = call_command("application-add", args=[name], as_json={1})
    application = models.Application.objects.get(name=name)
    assert isinstance(out, dict)
    assert ret == 0
    assert out == {
      "id": str(application.id),
      "name": name,
      "apikey": application.apikey,
      "active": True,
    }
    assert err == ""
    # command: show-stats (with application -added- previously)
    self.test_show_stats(applications=[application])
    return application

  def test_application_disable(self, name="app"):
    application = self.test_application_add(name=name)
    # command: application-disable
    ret, out, err = call_command("application-disable", args=[str(application.id)], as_json={1})
    assert ret == 0
    assert out == {
      "id": str(application.id),
      "name": name,
      "apikey": application.apikey,
      "active": False,
    }
    assert err == ""
    # command: show-stats (with application -disabled- previously)
    application.active = False
    self.test_show_stats(applications=[application])
    return application

  def test_show_stats(self, *, applications=[]):
    ret, out, err = call_command("show-stats", as_json={1})
    assert ret == 0
    assert out == {
      "application": {
        "count": len(applications),
        "items": [{
          "id": str(application.id),
          "name": application.name,
          "apikey": application.apikey,
          "active": application.active,
        } for application in applications]
      }
    }
    assert err == ""


class TestFail:

  def test_application_add(self, name="app"):
    # missing required argument: name
    with pytest.raises(CommandError, match="Error: the following arguments are required: name"):
      call_command("application-add")

    # duplicated argument: name
    call_command("application-add", args=[name])
    ret, out, err = call_command("application-add", args=[name], as_json={2})
    assert ret == 1
    assert out == ""
    assert err == {
      "err": "IntegrityError",
      "msg": "\n".join([
        'duplicate key value violates unique constraint "oculus_application_name_key"',
        'DETAIL:  Key (name)=(app) already exists.',
      ])
    }

  def test_application_disable(self, name="app"):
    # missing required argument: id
    with pytest.raises(CommandError, match="Error: the following arguments are required: id"):
      call_command("application-disable")

    # invalid argument: id (type)
    with pytest.raises(CommandError, match="Error: argument id: invalid UUID value: 'not-a-uuid'"):
      call_command("application-disable", args=["not-a-uuid"])

    # argument: id (non existing)
    ret, out, err = call_command("application-disable", args=["11111111-2222-3333-4444-555555555555"], as_json={2})
    assert ret == 1
    assert out == ""
    assert err == {
      "err": "DoesNotExist",
      "msg": "Application matching query does not exist.",
    }
