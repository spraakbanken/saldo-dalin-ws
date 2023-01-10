

.default: help

.PHONY: help
help:
	@echo "usage:"
	@echo "install-dev (alias: dev)"
	@echo "		installs the project for development"

	@echo "install"
	@echo "		installs the project for deployment"

	@echo "test"
	@echo "		run all tests"

	@echo "test-w-coverage"
	@echo "		run all tests with coverage information"

	@echo "lint"
	@echo "		lint all code"

	@echo "fmt"
	@echo "		format all python files"

	@echo "check-fmt"
	@echo "		check formatting for all python files"

dev: install-dev
install-dev:
	poetry install

install:
	poetry install --only main

.PHONY: test
test:
	poetry run pytest -vv

.PHONY: test-w-coverage
test-w-coverage:
	poetry run pytest -vv --cov=webapp --cov=sblex --cov-report=xml

.PHONY: lint
lint:
	poetry run pylint --rcfile=.pylintrc sb_auth_jwt tests

fmt:
	poetry run black .

.PHONY: check-fmt
check-fmt:
	poetry run black --check .
