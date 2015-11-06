
from ajax_select import registry
from ajax_select.registry import get_model
from django.contrib.admin import site
from django.contrib.admin.options import IS_POPUP_VAR
from django.http import HttpResponse
from django.utils.encoding import force_text
import json


def ajax_lookup(request, channel):

    """Load the named lookup channel and lookup matching models.

    GET or POST should contain 'term'

    Returns:
        HttpResponse - JSON: `[{pk: value: match: repr:}, ...]`
    Raises:
        PermissionDenied - depending on the LookupChannel's implementation of check_auth
    """

    # it should come in as GET unless global $.ajaxSetup({type:"POST"}) has been set
    # in which case we'll support POST
    if request.method == "GET":
        # we could also insist on an ajax request
        if 'term' not in request.GET:
            return HttpResponse('')
        query = request.GET['term']
    else:
        if 'term' not in request.POST:
            return HttpResponse('')  # suspicious
        query = request.POST['term']

    lookup = registry.get(channel)
    if hasattr(lookup, 'check_auth'):
        lookup.check_auth(request)

    if len(query) >= getattr(lookup, 'min_length', 1):
        instances = lookup.get_query(query, request)
    else:
        instances = []

    results = json.dumps([
        {
            'pk': force_text(getattr(item, 'pk', None)),
            'value': lookup.get_result(item),
            'match': lookup.format_match(item),
            'repr': lookup.format_item_display(item)
        } for item in instances
    ])

    return HttpResponse(results, content_type='application/json')


def add_popup(request, app_label, model):
    """Presents the admin site popup add view (when you click the green +).

    It serves the admin.add_view under a different URL and does some magic fiddling
    to close the popup window after saving and call back to the opening window.

    make sure that you have added ajax_select.urls to your urls.py::
        (r'^ajax_select/', include('ajax_select.urls')),

    this URL is expected in the code below, so it won't work under a different path
    TODO - check if this is still true.

    This view then hijacks the result that the django admin returns
    and instead of calling django's dismissAddAnontherPopup(win,newId,newRepr)
    it calls didAddPopup(win,newId,newRepr) which was added inline with bootstrap.html
    """

    themodel = get_model(app_label, model)
    admin = site._registry[themodel]

    # TODO : should detect where we really are
    # admin.admin_site.root_path = "/ajax_select/"

    # Force the add_view to always recognise that it is being
    # rendered in a pop up context
    if request.method == 'GET':
        get = request.GET.copy()
        get[IS_POPUP_VAR] = 1
        request.GET = get
    elif request.method == 'POST':
        post = request.POST.copy()
        post[IS_POPUP_VAR] = 1
        request.POST = post

    response = admin.add_view(request, request.path)

    if request.method == 'POST' and (response.status_code == 200):

        def fiddle(response):
            content = response.content.decode('UTF-8')
            # django >= 1.8
            fiddled = content.replace('dismissAddRelatedObjectPopup', 'didAddPopup')
            # django < 1.8
            fiddled = fiddled.replace('dismissAddAnotherPopup', 'didAddPopup')
            response.content = fiddled.encode('UTF-8')
            return response

        response.add_post_render_callback(fiddle)

    return response
