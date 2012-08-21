
# creates a virtualenv and installs a django here
virtualenv AJAXSELECTS
source AJAXSELECTS/bin/activate
pip install django

# put ajax selects in the path
ln -s ../ajax_select/ ./ajax_select

# create sqllite database
./manage.py syncdb

echo "type 'source AJAXSELECTS/bin/activate' to activate the virtualenv"
echo "then run: ./manage.py runserver"
echo "and visit http://127.0.0.1:8000/admin/"
echo "type 'deactivate' to close the virtualenv or just close the shell"

