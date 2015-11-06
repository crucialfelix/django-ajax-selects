Contributing
============


Testing
-------

For any pull requests you should run the unit tests first. Travis CI will also run all tests across all supported versions against your pull request and github will show you the failures.

Its much faster to run them yourself locally.::

    pip install -r requirements-test.txt

run tox:::

    make test

    # or just
    tox

With all supported combinations of Django and Python.

You will need to have different Python interpreters installed which you can do with:

https://github.com/yyuu/pyenv

It will skip tests for any interpreter you don't have installed.

Most importantly you should have at least 2.7 and 3.4


Documentation
-------------

Docstrings use Google style: http://sphinx-doc.org/ext/example_google.html#example-google
