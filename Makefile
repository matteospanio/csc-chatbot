UNAME := $(shell uname)
POETRY := poetry run

ifeq ($(UNAME), Linux)
	OPEN = xdg-open
endif
ifeq ($(UNAME), Darwin)
	OPEN = open
endif
ifeq ($(UNAME), Windows)
	OPEN = start
endif

default: help

.PHONY: help
help: ## Show this help
	@$(POETRY) python scripts/print_make_help.py < $(MAKEFILE_LIST)

.PHONY: clean
clean: ## remove all build, test, coverage and Python artifacts
	@$(POETRY) bash scripts/clean.sh
	$(POETRY) ruff clean

.PHONY: format
format: ## format code
	@echo "Format docstrings"
	@$(POETRY) docformatter --config ./pyproject.toml --in-place ./src ./tests
	@echo "Format code with black"
	@$(POETRY) black .

.PHONY: lint
lint: ## check style with pylint
	$(POETRY) ruff check ./src ./tests --fix

.PHONY: update
update: ## update dependencies
	poetry update
	$(POETRY) pre-commit autoupdate

.PHONY: install
install: ## install the package to the active Python's site-packages
	@poetry install
	@$(POETRY) pre-commit install

.PHONY: test
test: ## run tests quickly with the default Python
	@echo "Run test suite"
	@$(POETRY) bash scripts/run_tests.sh

htmlcov: ## create HTML coverage report
	@$(POETRY) pytest --cov-report html --cov=src --cov-report term
	$(OPEN) htmlcov/index.html
