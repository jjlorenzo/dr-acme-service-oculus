#!/usr/bin/env sh

set -x

docker compose down --remove-orphans --volumes
docker compose up --remove-orphans --renew-anon-volumes --no-start
docker compose up postgres --detach
docker compose up rabbitmq --detach

poetry build -f sdist
VERSION=$(poetry run python -c "import acme.service.oculus ; print(acme.service.oculus.__version__, end='')")
docker compose run --rm python mkdir -p /opt/dist
docker compose run --rm --volume=./dist:/dist python cp /dist/acme.service.oculus-"${VERSION}".tar.gz /opt/dist/
rm -rf dist/*

docker compose run --rm python python -m venv /opt/venv
docker compose run --rm python python -m pip install --upgrade pip
docker compose run --rm python pip install /opt/dist/acme.service.oculus-"${VERSION}".tar.gz

until docker compose exec postgres pg_isready --quiet; do
  echo "Waiting for (oculus-postgres) PostgreSQL..."
  sleep 1
done

docker compose run --rm python django-admin migrate

exec docker compose up --detach
