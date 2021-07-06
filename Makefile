REQS_IN = core/requirements.in
REQS_OUT = core/requirements.txt

requirements:
	pip-compile $(REQS_IN) -o $(REQS_OUT)

format:
	isort .
	black .

type:
	mypy .

makemigrations:
	docker-compose run dsa_smart pem watch --traceback

migrate:
	docker-compose run dsa_smart pem migrate
