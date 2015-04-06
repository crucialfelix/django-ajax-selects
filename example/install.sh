#!/bin/sh

# break on any error
set -e

# creates a virtualenv
virtualenv AJAXSELECTS
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

echo "Creating a sqllite database:"
./manage.py syncdb

echo "\nto activate the virtualenv:\nsource AJAXSELECTS/bin/activate"

echo '\nto create an admin account:'
echo './manage.py createsuperuser'

echo "\nto run the testserver:\n./manage.py runserver"
echo "\nthen open this url:\nhttp://127.0.0.1:8000/admin/"
echo "\nto close the virtualenv or just close the shell:\ndeactivate"

exit 0
