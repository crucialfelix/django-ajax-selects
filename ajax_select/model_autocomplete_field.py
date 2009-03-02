# -*- coding: utf-8 -*-

# based on http://www.djangosnippets.org/snippets/1097/

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList, ValidationError
from ajax_select import get_lookup

CLIENT_CODE = """
<input type="text" name="%(name)s_text" id="%(html_id)s_text" value="%(current_name)s" size="40" />
<input type="hidden" name="%(name)s" id="%(html_id)s" value="%(current_id)s" />
<script type="text/javascript">
$(function(){
	function formatItem_%(html_id)s(row) {
		return row[2];
	}
	function formatResult_%(html_id)s(row) {
        return row[1];
	}
	$("#%(html_id)s_text").autocomplete('%(lookup_url)s', {
		width: 320,
		formatItem: formatItem_%(html_id)s,
		formatResult: formatResult_%(html_id)s
	});
	$("#%(html_id)s_text").result(function(event, data, formatted) {
        $("#%(html_id)s").val(data[0]);
        $("#%(html_id)s_text").val(data[1]);
	});
	$("#%(html_id)s_text").blur(function() {
	    if(! $("#%(html_id)s_text").val() ){
	        $("#%(html_id)s").val('');
	    }
	});
});
</script>
"""

class ModelAutoCompleteWidget(forms.widgets.TextInput):
    """ widget autocomplete for text fields
    """

    html_id = ''

    def __init__(self,
                 channel,
                 *args, **kw):
        super(forms.widgets.TextInput, self).__init__(*args, **kw)
        # url for Datasource
        self.channel = channel

    def render(self, name, value, attrs=None):
        if value == None:
            value = ''
        html_id = attrs.get('id', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        if value:
            current_name = lookup.get_objects([value])[0]
        else:
            current_name = ''
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})
        return mark_safe(CLIENT_CODE % dict(name=name, html_id=html_id,lookup_url=lookup_url,current_id=value,current_name=current_name))

    def value_from_datadict(self, data, files, name):

        got = data.get(name, None)
        if got:
            return long(got)
        else:
            return None




class ModelAutoCompleteField(forms.fields.CharField):
    """
    Autocomplete form field for Model
    """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        super(ModelAutoCompleteField, self).__init__(
            widget = ModelAutoCompleteWidget(channel=channel),
            max_length=255,
            *args, **kwargs)

    def clean(self, value):
        return value # id of object
        # possible error condition if someone else deleted object while you editing


