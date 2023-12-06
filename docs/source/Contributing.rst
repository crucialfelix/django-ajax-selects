Contributing
============


Testing
-------

Github workflows will also run all tests across all supported versions against your pull request and github will show you the failures.

To run them locally::

    pipenv install
    pipenv shell
    make test

With all supported combinations of Django and Python.

You will need to have different Python interpreters installed which you can do with:

https://github.com/yyuu/pyenv

It will skip tests for any interpreter you don't have installed.

Most importantly you should have at least Python 3.10


Documentation
-------------

Docstrings use Google style: http://sphinx-doc.org/ext/example_google.html#example-google
