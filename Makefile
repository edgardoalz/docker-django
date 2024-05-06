SHELL=/bin/bash
# Black magic to get module directories
PYTHON_MODULES := $(foreach initpy, $(foreach dir, $(wildcard ./*), $(wildcard $(dir)/__init__.py)), $(realpath $(dir $(initpy))))

lint:
	ruff check$(PYTHON_MODULES)

lint_fix:
	ruff check$(PYTHON_MODULES) --fix

check_format:
	ruff format$(PYTHON_MODULES) --check

format:
	ruff format$(PYTHON_MODULES)

lint_github:
	ruff check$(PYTHON_MODULES) --output-format=github
