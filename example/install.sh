#!/bin/sh

# break on any error
set -e

# creates a virtualenv
virtualenv AJAXSELECTS
source AJAXSELECTS/bin/activate

DJANGO=$1
if [ "$DJANGO" != "" ]; then
    echo "Installing Django $DJANGO"
    pip install Django==$DJANGO
else
    echo "Installing latest django"
    pip install django
fi

echo "Creating a sqllite database"
./manage.py syncdb

if [ ! -d ./ajax_select ]; then
	echo "\nSymlinking ajax_select into this app directory"
	ln -s ../ajax_select/ ./ajax_select
fi

echo "\ntype 'source AJAXSELECTS/bin/activate' to activate the virtualenv"

echo '\ncreate an admin account:'
echo './manage.py createsuperuser'

echo "\nrun: ./manage.py runserver"
echo "and visit http://127.0.0.1:8000/admin/"
echo "\ntype 'deactivate' to close the virtualenv or just close the shell"

exit 0
