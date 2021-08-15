help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests"
	@echo "install - install the package to the user's Python's site-packages"
	@echo "help - show this help and exit"

clean:
	@rm -rf build dist *.egg-info
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -rf .tox
	@rm -f src/*.egg*

lint:
	@flake8 speedypy

test:
	@tox

docs:
	@echo "Not yet implemented"

install:
	python3 setup.py install --user

.PHONY: build clean lint test docs deploy install help
