
from ajax_select import get_lookup
from django.contrib.admin import site
from django.db import models
from django.http import HttpResponse
try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.utils.encoding import force_text


def ajax_lookup(request, channel):

    """ this view supplies results for foreign keys and many to many fields """

    # it should come in as GET unless global $.ajaxSetup({type:"POST"}) has been set
    # or the user defined in either the global settings or the lookup or a form field
    # that either a GET or POST must be used. defaults to GET.
    # we could also insist on an ajax request
    requestVars = request.GET
    if request.method == "POST":
        requestVars = request.POST

    if 'term' not in requestVars:
        return HttpResponse('')  # suspicious

    query = requestVars.get('term', '')
    limit = requestVars.get('limit', None)
    offset = requestVars.get('offset', None)

    lookup = get_lookup(channel)
    if hasattr(lookup, 'check_auth'):
        lookup.check_auth(request)

    instances = []
    if len(query) >= getattr(lookup, 'min_length', 1):

        instances = lookup.get_query(query, request, offset=offset, limit=limit)

    # stream out the result rather than making this a clob first
    def dump_results(instances) :

        index = 0
        itemCount = len(instances)

        yield '['

        for item in instances:

            yield json.dumps({
                'pk': force_text(getattr(item, 'pk', None)),
                'value': lookup.get_result(item),
                'match': lookup.format_match(item),
                'repr': lookup.format_item_display(item)
            })

            if index < itemCount - 1:

                yield ','

            index = index + 1

        yield ']'

    return HttpResponse(dump_results(instances), 
                        content_type='application/javascript')


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
        try:
            # this detects TemplateResponse which are not yet rendered
            # and are returned for form validation errors
            if not response.is_rendered:
                out = response.rendered_content
            else:
                out = response.content
        except AttributeError:  # django < 1.5
            out = response.content
        if 'opener.dismissAddAnotherPopup' in out:
            return HttpResponse(out.replace('dismissAddAnotherPopup', 'didAddPopup'))
    return response
