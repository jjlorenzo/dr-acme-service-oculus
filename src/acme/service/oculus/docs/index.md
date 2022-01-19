# Overview

## What is `acme.service.oculus`?

A service that collect user behaviour events from multiple applications, aggregates and allows to query the information.

## Assumptions

- For recognizing `Applications` as "trusted-clients" I use a simpler mechanism of sharing an ApiKey, that impl could be
  improved with a more secure mechanism, right now is just a signed value that can be unsigned with django `SECRET_KEY`.
  I don't include other imrpovements here because it is for now a POC, but later this `SECRET_KEY` must be configurable
  instead of a hard-coded value. Probably it worth to take a look at 
  [djangorestframework-api-key](https://pypi.org/project/djangorestframework-api-key/) for a more secure implementation.
- Since the system will receive a lot of traffic from `Applications`, the event processing is async using `celery` as
  the distributed task queue. Instead of ensuring that multiple workers doesn't process the same event at the same time
  I follow a simpler approach for now, ensuring that doesn't exists duplicated events.
- For preventing duplicated events, I use a db contrains, using all fields of the event, another alternative could be
  generating a hash for event at ingress time, but inpacts the performance of the ingress process for all events.
- For the ingress process I prefer a simpler implementation that doesn't use to much features from celery except
  the async task processing, of course. So instead of using a result backend, I manually store errors that can arrise
  in the process.
- For the anaylics endpoints, I just implement the one related to the `Event`, and I choose to stick with rest-framework
  as simpler as possible, not using `GenericViewSet` nor `ModelSerializer`, because imho in this case it doesn't worth
  the magic that they introduce.

## Interfaces

The application has two kind of interfaces: (`cli` and `http`)

- `cli`: to be used by admins for `Applications` management, etc.
- `http.analytics`: to be used by analytics team
- `http.ingress`: to be used by `Applications` for `Event` submission

## TODO

- I think that could be interesting to relate the `Event` with the `Application`, so you can search for an specific 
  `Application`.
- `ResultError` query interface, either `http` or `cli`.
- Complete the testsuite, covering the `ingress` process.

## Contributing

For local development I use [poetry](https://python-poetry.org/) and services that I have locally installed in
my workstation, e.g. postgres, rabbitmq, etc. But if you prefer something based on docker, you can take a look at 
`docker-compose.sh`, it's a simpler container orchestration that runs the whole stack with an approach that I tend to 
use where I don't build images, but use the containers as artifacts builders and runners, e.g. the aretifacts are stored
in docker named volumes.

### Summary of the output of `docker-compose.sh`:

```sh
$ ./docker-compose.sh

+ docker compose down --remove-orphans --volumes

+ docker compose up --remove-orphans --renew-anon-volumes --no-start
[+] Running 8/8
 ⠿ Network oculus                                      Created       0.0s
 ⠿ Volume "oculus--rabbitmq--var-lib-rabbitmq"         Created       0.0s
 ⠿ Volume "oculus--python--opt"                        Created       0.0s
 ⠿ Volume "oculus--postgres--var-lib-postgresql-data"  Created       0.0s
 ⠿ Container oculus-python                             Created       0.1s
 ⠿ Container oculus-postgres                           Created       0.1s
 ⠿ Container oculus-celery                             Created       0.1s
 ⠿ Container oculus-rabbitmq                           Created       0.1s

+ docker compose up postgres --detach
[+] Running 1/1
 ⠿ Container oculus-postgres  Started                                0.3s

+ docker compose up rabbitmq --detach
[+] Running 1/1
 ⠿ Container oculus-rabbitmq  Started                                0.4s

+ poetry build -f sdist
Building acme.service.oculus (0.1.0)
  - Building sdist
  - Built acme.service.oculus-0.1.0.tar.gz

+ docker compose run --rm python mkdir -p /opt/dist

+ docker compose run --rm --volume=./dist:/dist python cp /dist/acme.service.oculus-0.1.0.tar.gz /opt/dist/

+ rm -rf dist/acme.service.oculus-0.1.0.tar.gz

+ docker compose run --rm python python -m venv /opt/venv

+ docker compose run --rm python python -m pip install --upgrade pip
...
Successfully installed pip-21.3.1

+ docker compose run --rm python pip install /opt/dist/acme.service.oculus-0.1.0.tar.gz
...
Successfully installed acme.service.oculus-0.1.0 ...


+ docker compose exec postgres pg_isready --quiet

+ docker compose run --rm python django-admin migrate
Operations to perform:
  Apply all migrations: oculus
Running migrations:
  Applying oculus.0001_create_model_application... OK
  Applying oculus.0002_create_model_event... OK
  Applying oculus.0003_create_model_result_error... OK
  Applying oculus.0004_create_constraint_event-unique... OK

+ exec docker compose up --detach
[+] Running 4/4
 ⠿ Container oculus-postgres  Running                                0.0s
 ⠿ Container oculus-rabbitmq  Running                                0.0s
 ⠿ Container oculus-celery    Started                                0.3s
 ⠿ Container oculus-python    Started
```
