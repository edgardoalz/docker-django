SHELL=/bin/bash

venv:
	rm -rf .venv
	python -m venv .venv
	. .venv/bin/activate
install_dev:
	make venv
	pip install -r requirements-dev.txt
	pre-commit install
validate_code:
	pre-commit run --all