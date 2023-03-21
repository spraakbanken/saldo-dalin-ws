deafult: test

INVENV := if env_var_or_default('VIRTUAL_ENV', "") == "" { "poetry run" } else { "" }


alias dev := install-dev
# installs the project for development
install-dev:
	poetry install

# installs the project for deployment
install:
	poetry install --only main



default-cov := "--cov=sblex"
cov-report := "term-missing"
cov := default-cov

# run given test(s)
test *tests="test/components":
	{{INVENV}} pytest -vv {{tests}}

# run given test(s) with coverage information
test-w-coverage +tests="test":
	{{INVENV}} pytest -vv {{cov}} --cov-report={{cov-report}} {{tests}}

# lint all code
lint:
	{{INVENV}} ruff components bases sblex test

# format all python files
fmt:
	{{INVENV}} black components bases sblex test

# check formatting for all python files
check-fmt:
	{{INVENV}} black --check components bases sblex test
