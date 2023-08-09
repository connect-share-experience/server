#################### LOCAL CI ####################

COVERAGE=10
PYLINT_TRESHOLD=9
SOURCES = "app app/models app/utils app/exceptions"

.PHONY: install-dependencies linting

# DEPENDECIES

install-dependencies:
	pip install -r requirements.txt


# LINTING

app-linting-basic:
	@echo "$(bold)$(blue)=============== flake8 on app ===============$(normal)"
	python -m flake8 app

app-linting-extensive:
	@echo "$(bold)$(blue)=============== pylint on app ===============$(normal)"
	cd app && pylint_runner -v --fail-under=${PYLINT_TRESHOLD}

tests-linting-basic:
	@echo "$(bold)$(blue)=============== flake8 on tests ===============$(normal)"
	python -m flake8 tests

tests-linting-extensive:
	@echo "$(bold)$(blue)=============== pylint on tests ===============$(normal)"
	cd tests && pylint_runner -v --fail-under=${PYLINT_TRESHOLD}


# TYPE HINT CHECKING

type-hint-checking:
	@echo "$(bold)$(green)=============== mypy on app ===============$(normal)"
	python -m mypy app


# SECURITY

source-code-security:
	@echo "$(bold)$(purple)=============== bandit ===============$(normal)"
	python -m bandit -r app

dependencies-security:
	@echo "$(bold)$(yellow)=============== safety ===============$(normal)"
	safety check --ignore=51668


# TESTS

testing:
	@echo "$(bold)$(cyan)=============== pytest ===============$(normal)"
	pytest --cov=app --cov-fail-under=${COVERAGE} --cov-report term-missing


# MACROS

linting-app: app-linting-basic app-linting-extensive
linting-tests : tests-linting-basic tests-linting-extensive

full-syntax-app: linting-app type-hint-checking

security-check: source-code-security dependencies-security

run-pipe: full-syntax-app security-check testing

run-full-pipe: full-syntax-app linting-tests security-check testing

run-full-pipe-and-dep: install-dependencies run-full-pipe
