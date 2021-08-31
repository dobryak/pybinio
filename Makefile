PYTHON := python3.9
BIN := env/bin

.PHONY: env
env:
	@$(PYTHON) -m venv env
	@$(BIN)/$(PYTHON) -m pip install isort flake8 mypy wheel black

.PHONY: check
check: tests flake8 isort-check black-check mypy-check

.PHONY: style
style: isort black

.PHONY: tests
tests:
	@$(BIN)/$(PYTHON) -m unittest

.PHONY: isort
isort:
	@$(BIN)/$(PYTHON) -m isort binio tests

.PHONY: black
black:
	@$(BIN)/$(PYTHON) -m black binio tests

.PHONY: flake8
flake8:
	@$(BIN)/$(PYTHON) -m flake8 binio tests

.PHONY: isort-check
isort-check:
	@$(BIN)/$(PYTHON) -m isort -c binio tests

.PHONY: black-check
black-check:
	@$(BIN)/$(PYTHON) -m black --check binio tests

.PHONY: mypy-check
mypy-check:
	@$(BIN)/$(PYTHON) -m mypy --strict binio tests

.PHONY: dist
dist:
	@$(BIN)/$(PYTHON) setup.py bdist_wheel bdist
