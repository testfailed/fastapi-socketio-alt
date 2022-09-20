.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: build
build:				## Build the project.
	@poetry build -vvv

.PHONY: clean
clean:				## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: format
format:				## Format code using black & isort.
	$(ENV_PREFIX)black fastapi_socketio/
	$(ENV_PREFIX)black tests/

.PHONY: help
help:				## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: info
info:				## Show the current environment infomations.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@poetry env info
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: install
install:			## Install the project in production environment.
		poetry lock -vvv &&
			poetry install -vvv

.PHONY: install-all
install-all:			## Install the project in development environment.
		poetry lock -vvv &&
			poetry install --all-extras -vvv

.PHONY: lint
lint:				## Run black linter.
	$(ENV_PREFIX)black --check fastapi_socketio/
	$(ENV_PREFIX)black --check tests/

.PHONY: test
test: lint			## Run pytest.
	$(ENV_PREFIX)pytest -v -l --tb=short --maxfail=1 tests/

.PHONY: test-watch
test-watch:			## Run and watch pytest.
	ls **/**.py | entr $(ENV_PREFIX)pytest --picked=first -s -vvv -l --tb=long --maxfail=1 tests/
