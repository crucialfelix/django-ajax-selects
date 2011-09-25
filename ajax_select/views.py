
from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson


def ajax_lookup(request,channel):
    """ this view supplies results for both foreign keys and many to many fields """

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

    if len(query) >= getattr(lookup, 'min_length', 1):
        instances = lookup.get_query(query,request)
    else:
        instances = []

    results = simplejson.dumps([
        { 'pk': unicode(item.pk), 'label': lookup.format_result(item),
            'desc': lookup.format_item(item) }
        for item in instances
    ])

    return HttpResponse(results, mimetype='application/javascript')


def add_popup(request,app_label,model):
    """ present an admin site add view, hijacking the result if its the dismissAddAnotherPopup js and returning didAddPopup """
    themodel = models.get_model(app_label, model)
    admin = site._registry[themodel]

    admin.admin_site.root_path = "/ajax_select/" # warning: your URL should be configured here.
    # as in your root urls.py includes :
    #    (r'^ajax_select/', include('ajax_select.urls')),
    # I should be able to auto-figure this out but ...

    response = admin.add_view(request,request.path)
    if request.method == 'POST':
        if response.content.startswith('<script type="text/javascript">opener.dismissAddAnotherPopup'):
            return HttpResponse( response.content.replace('dismissAddAnotherPopup','didAddPopup' ) )
    return response

