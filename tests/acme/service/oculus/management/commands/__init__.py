import django.core.management
import io
import json
import pytest
import typing


def call_command(name: str, *, args=[], as_json={}) -> typing.Tuple[int, dict[str, str] | str, dict[str, str] | str]:
  stdout = io.StringIO()
  stderr = io.StringIO()
  with pytest.raises(SystemExit) as sys_exit:
    django.core.management.call_command(name, *args, stdout=stdout, stderr=stderr)

  valout = stdout.getvalue()
  if 1 in as_json:
    valout = json.loads(valout)

  valerr = stderr.getvalue()
  if 2 in as_json:
    valerr = json.loads(valerr)

  return (
    sys_exit.value.code,
    valout,
    valerr,
  )
