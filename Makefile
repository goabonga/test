# define the name of the virtual environment directory
VENV := .venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: setup.py
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e ./[dev]

# venv is a shortcut target
venv: $(VENV)/bin/activate

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rv {} +
	find . -type d -name 'build' -exec rm -rv {} +
	find . -type d -name '*.egg-info' -exec rm -rv {} +
	rm -Rf htmlcov

lint: venv
	$(VENV)/bin/isort ./
	$(VENV)/bin/black ./
	$(VENV)/bin/autoflake --in-place --remove-duplicate-keys --remove-unused-variables --remove-all-unused-imports -r ./

test: venv
	$(VENV)/bin/pytest

coverage: venv
	$(VENV)/bin/pytest --cov-report=term --cov=playground tests/

all: lint test

.PHONY: all venv clean lint test
