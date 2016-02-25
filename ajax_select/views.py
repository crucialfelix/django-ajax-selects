
from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse
import json


def ajax_lookup(request, channel):

    """ this view supplies results for foreign keys and many to many fields """

    query = request.GET.get('term') or request.GET.get('q') or request.POST.get('term') or request.POST.get('q')

    if query is None:
        return HttpResponse('')

    lookup = get_lookup(channel)
    if hasattr(lookup, 'check_auth'):
        lookup.check_auth(request)

    if len(query) >= getattr(lookup, 'min_length', 1):
        instances = lookup.get_query(query, request)
    else:
        instances = []

    def origin(item):
        origlu = getattr(item, 'origin', None)
        if not origlu:
            return None
        return origlu.model.__name__

    results = json.dumps([
        {
            'pk': unicode(getattr(item, 'pk', None)),
            'value': lookup.get_result(item),
            'match': lookup.format_match(item),
            'repr': lookup.format_item_display(item),
            'origin': origin(item),
        } for item in instances
    ])

    return HttpResponse(results, content_type='application/javascript')


def add_popup(request, app_label, model):
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

    response = admin.add_view(request, request.path)
    if request.method == 'POST':
        if 'opener.dismissAddAnotherPopup' in unicode(response.content):
            return HttpResponse(response.content.replace('dismissAddAnotherPopup', 'didAddPopup'))
    return response
