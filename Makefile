.PHONY: clean-pyc clean-build
# docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the currently installed Django"
	@echo "testall - run tests on every Django version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 .

test:
	tox

coverage:
	coverage run --source ajax_select runtests.py
	coverage report -m
	coverage html
	open htmlcov/index.html

# docs:
# 	rm -f docs/django-ajax-selects.rst
# 	rm -f docs/modules.rst
# 	sphinx-apidoc -o docs/ django-ajax-selects
# 	$(MAKE) -C docs clean
# 	$(MAKE) -C docs html
# 	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean
	python setup.py sdist
	ls -l dist
