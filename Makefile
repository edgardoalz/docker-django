SHELL=/bin/bash

install_dev:
	pip install -r requirements/dev.txt
	pre-commit install
validate_code:
	pre-commit run --all