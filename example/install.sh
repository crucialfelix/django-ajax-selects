
# creates a virtualenv and installs a django here
virtualenv AJAXSELECTS
source AJAXSELECTS/bin/activate
easy_install django

# put ajax selects in the path
ln -s ../ajax_select/ ./ajax_select

# create sqllite database
./manage.py syncdb

echo "type 'deactivate' to close the virtualenv"
echo "type 'source AJAXSELECTS/bin/activate' to reactivate it"

