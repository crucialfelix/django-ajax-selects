
from django import forms
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings
from ajax_select import get_lookup

CLIENT_CODE = """
<input type="text" name="%(name)s_text" id="%(html_id)s_text" value="%(current_name)s" size="40" />
<p class="help">Enter a search term to lookup.%(help_text)s</p>
<p id="%(html_id)s_on_deck" class="results_on_deck"></p>
<input type="hidden" name="%(name)s" id="%(html_id)s" value="%(current_ids)s" />
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
		multiple: true,
		multipleSeparator: " ",
		scroll: true,
		scrollHeight:  300,
		formatItem: formatItem_%(html_id)s,
		formatResult: formatResult_%(html_id)s
	});
	$("#%(html_id)s_text").result(function(event, data, formatted) {
	    id = data[0];
	    if( $("#%(html_id)s").val().indexOf( "|"+id+"|" ) == -1) {
	        if($("#%(html_id)s").val() == '') {
	            $("#%(html_id)s").val('|');
	        }
	        $("#%(html_id)s").val( $("#%(html_id)s").val() + id + "|");
	        addKiller_%(html_id)s(data[1],id);
	    }
	});
	function addKiller_%(html_id)s(repr,id) {
        kill = "<span class='iconic' id='kill_" + id + "'>X</span>  ";
        $( "#%(html_id)s_on_deck" ).append("<div id='%(html_id)s_on_deck_" + id +"'>" + kill + repr + " </div>");
        $("#kill_"+id).click(function(num) { return function(){kill_%(html_id)s(num)}}(id) );
	}
	function kill_%(html_id)s(id) {
	    $("#%(html_id)s").val( $("#%(html_id)s").val().replace( "|" + id + "|", "|" ) );
	    $("#%(html_id)s_on_deck_" + id).remove();
	}
	currentRepr = %(current_reprs)s;
	currentRepr.forEach(function(its){
	    addKiller_%(html_id)s(its[0],its[1]);
	});
});
</script>"""




class MultiAutoCompleteWidget(forms.widgets.SelectMultiple):

    html_id = ''
    
    def __init__(self,
                 channel,
                 help_text='',
                 *args, **kw):
        super(MultiAutoCompleteWidget, self).__init__(*args, **kw)
        self.channel = channel
        self.help_text = help_text

    def render(self, name, value, attrs=None):
        if value == None:
            value = []
        html_id = attrs.get('id', name)
        self.html_id = html_id

        lookup = get_lookup(self.channel)
        lookup_url = reverse('ajax_lookup',kwargs={'channel':self.channel})

        current_name = ""# the text field starts empty
        # value = [3002L, 1194L]
        if value:
            current_ids = "|" + "|".join( str(id) for id in value ) + "|" # id|id of current
        else:
            current_ids = "|"
        
        objects = lookup.get_objects(value)
        
        # text repr of currently selected items
        current_repr = []
        current_repr_json = []
        for obj in objects:
            repr = lookup.format_item(obj)
            current_repr_json.append( """new Array("%s",%s)""" % (repr,obj.id) )

        current_reprs = "new Array(%s)" % ",".join(current_repr_json)
        
        vars = dict(name=name,
         html_id=html_id,
         lookup_url=lookup_url,
         current=value,
         current_name=current_name,
         current_ids=current_ids,
         current_reprs=current_reprs,
         help_text=self.help_text
         )
        return mark_safe(CLIENT_CODE % vars)


    def value_from_datadict(self, data, files, name):
        #eg u'members': [u'|229|4688|190|']
        return [long(val) for val in data.get(name,'').split('|') if val]




class MultiAutoCompleteField(forms.fields.CharField):
    """
        channel: eg. 'contact', a key for settings.AJAX_LOOKUP_CHANNELS
            which returns a Lookup object that implements:
            
    def get_query(self,q,request):
        return Contact.objects.filter(name__startswith=q)
    
    def format_item(self,contact):
        return unicode(contact)

    def format_result(self,contact):
        return u"%s %s (%s)" % (contact.fname, contact.lname,contact.email)

    def get_objects(self,ids):
        from peoplez.models import Contact
        return Contact.objects.filter(pk__in=ids).order_by('lname','fname')
    
    """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        kwargs['widget'] = MultiAutoCompleteWidget(channel=channel,help_text=kwargs.get('help_text',''))
        super(MultiAutoCompleteField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value # a list of IDs from widget value_from_datadict




