deafult: test

INVENV := if env_var_or_default('VIRTUAL_ENV', "") == "" { "poetry run" } else { "" }


alias dev := install-dev
# installs the project for development
install-dev:
	poetry install

# installs the project for deployment
install:
	poetry install --only main

# run all tests
test:
	{{INVENV}} pytest -vv

cov-report := "term-missing"

# run all tests with coverage information
test-w-coverage:
	{{INVENV}} pytest -vv --cov=sblex --cov-report={{cov-report}}

# lint all code
lint:
	{{INVENV}} ruff bases components

# format all python files
fmt:
	{{INVENV}} black .

# check formatting for all python files
check-fmt:
	{{INVENV}} black --check .
