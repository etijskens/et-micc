#-------------------------------------------------------------------------------
# This makefile automates a number of tasks for the developer of this Python
# package.
# This makefile is meant to be run in the project directory (not elsewhere) as:
#   > make <target>
#-------------------------------------------------------------------------------

module_name := micc

version := $(shell python -c 'from $(module_name) import __version__; print(__version__)')

site_packages := $(shell python -c "import site; print(site.getsitepackages()[0])")

cwd := $(shell pwd)

.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 --max-line-length=100 micc tests

test: ## run tests quickly with the default Python
	py.test tests/test*

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source micc -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/micc.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ micc
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

#-------------------------------------------------------------------------------
#-- INSTALLATION TARGETS -------------------------------------------------------
#-------------------------------------------------------------------------------
# Create distribution wheel
dist: clean
	poetry build

#-------------------------------------------------------------------------------
# Install package {{ cookiecutter.package_name }} to the active Python's site-packages
install: clean
	pip install dist/$(module_name)-$(version)-py3-none-any.whl

#-------------------------------------------------------------------------------
# Uninstall package {{ cookiecutter.package_name }} from current Python environment
uninstall:
	pip uninstall $(module_name)

#-------------------------------------------------------------------------------
# Install package {{ cookiecutter.package_name }} in development mode, so that edited changes in the 
# packages are immediately efficitive. This is achieved through a soft link.
#	pip install -e $(module_name)
install-dev: 
	ln -s $(cwd)/$(module_name) $(site_packages)/$(module_name)
	
#-------------------------------------------------------------------------------
# Uninstall package {{ cookiecutter.package_name }} development mode from the current Python environment
uninstall-dev:
	rm $(site_packages)/$(module_name)
