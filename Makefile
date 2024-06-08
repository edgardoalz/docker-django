SHELL=/bin/bash

install_dev:
	pip install -r requirements/dev.txt
	pre-commit install
validate_code:
	pre-commit run --all
docker_build:
	docker build -f Dockerfile -t finance-api:latest .
docker_run:
	docker run --env-file=./.env -p 8000:8000 --name finance_api --rm finance-api:latest
django_run:
	python manage.py runserver --bind "0.0.0.0:8080"
celery_worker:
	celery -A finance_api.tasks worker --autoscale=8,2 -l INFO
celery_beat:
	celery -A finance_api.tasks beat -l INFO
celery_flower:
	celery -A finance_api.tasks --broker="${BROKER_URL}" flower -l INFO
celery_repl:
	celery -A finance_api.tasks --broker="${BROKER_URL}" amqp repl