
# A test application to play with django-ajax-selects

## INSTALL

Install a local django in a virtualenv:

    ./install.sh

Or to install a specific django version:

    ./install.sh 5.0

List of available django versions:

https://pypi.python.org/pypi/Django

This will also activate the virtualenv and create a sqlite db

## VIRTUALENV

Active the virtualenv:

    source AJAXSELECTS/bin/activate


## Run the server

    ./manage.py runserver

Go visit the admin site and play around:

http://127.0.0.1:8000/admin

Try this page outside of the Django admin:

http://127.0.0.1:8000/search_form?