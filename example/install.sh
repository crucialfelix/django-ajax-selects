#!/bin/bash

# break on any error
set -e

# creates a virtualenv
virtualenv --no-site-packages AJAXSELECTS
source AJAXSELECTS/bin/activate

DJANGO=$1
if [ "$DJANGO" != "" ]; then
    echo "Installing Django $DJANGO:"
    pip install Django==$DJANGO
else
    echo "Installing latest django:"
    pip install django
fi

if [ ! -d ./ajax_select ]; then
	echo "\nSymlinking ajax_select into this app directory:"
	ln -s ../ajax_select/ ./ajax_select
fi

echo
echo "Creating a sqllite database:"
./manage.py migrate

echo
echo "Create example migrations"
./manage.py makemigrations example
./manage.py migrate example

echo
echo "to activate the virtualenv:"
echo "source AJAXSELECTS/bin/activate"

echo
echo 'to create an admin account:'
echo './manage.py createsuperuser'

echo
echo "to run the testserver:"
echo "./manage.py runserver"
echo
echo "then open this url:"
echo "http://127.0.0.1:8000/admin/"
echo
echo "to close the virtualenv or just close the shell:"
echo "deactivate"

exit 0
