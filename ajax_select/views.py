
from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson


def ajax_lookup(request,channel):

    """ this view supplies results for foreign keys and many to many fields """

    # it should come in as GET unless global $.ajaxSetup({type:"POST"}) has been set
    # in which case we'll support POST
    if request.method == "GET":
        # we could also insist on an ajax request
        if 'term' not in request.GET:
            return HttpResponse('')
        query = request.GET['term']
    else:
        if 'term' not in request.POST:
            return HttpResponse('') # suspicious
        query = request.POST['term']

    lookup = get_lookup(channel)
    if hasattr(lookup,'check_auth'):
        lookup.check_auth(request)

    if len(query) >= getattr(lookup, 'min_length', 1):
        instances = lookup.get_query(query,request)
    else:
        instances = []

    results = simplejson.dumps([
        {
            'pk': unicode(getattr(item,'pk',None)),
            'value': lookup.get_result(item),
            'match' : lookup.format_match(item),
            'repr': lookup.format_item_display(item)
        } for item in instances
    ])

    return HttpResponse(results, mimetype='application/javascript')


def add_popup(request,app_label,model):
    """ this presents the admin site popup add view (when you click the green +)

        make sure that you have added ajax_select.urls to your urls.py:
            (r'^ajax_select/', include('ajax_select.urls')),
        this URL is expected in the code below, so it won't work under a different path
        
        this view then hijacks the result that the django admin returns
        and instead of calling django's dismissAddAnontherPopup(win,newId,newRepr) 
        it calls didAddPopup(win,newId,newRepr) which was added inline with bootstrap.html
    """
    themodel = models.get_model(app_label, model)
    admin = site._registry[themodel]

    # TODO : should detect where we really are
    admin.admin_site.root_path = "/ajax_select/" 

    response = admin.add_view(request,request.path)
    if request.method == 'POST':
        if 'opener.dismissAddAnotherPopup' in response.content:
            return HttpResponse( response.content.replace('dismissAddAnotherPopup','didAddPopup' ) )
    return response

