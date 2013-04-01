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

echo "Symlinking ajax_select into this app directory"
ln -s ../ajax_select/ ./ajax_select

echo "Creating a sqllite database"
./manage.py syncdb

echo "run: ./manage.py runserver"
echo "and visit http://127.0.0.1:8000/admin/"
echo "type 'deactivate' to close the virtualenv or just close the shell"
echo "type 'source AJAXSELECTS/bin/activate' to re-activate the virtualenv"

exit 0
