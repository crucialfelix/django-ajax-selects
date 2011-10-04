/* {% comment %}
	the popup handler
	requires RelatedObjects.js which is part of the django admin js
	so if using outside of the admin then you would need to include that manually
{% endcomment %} */
if(typeof didAddPopup != 'function') {
	function didAddPopup(win,newId,newRepr) {
		var name = windowname_to_id(win.name);
		console.log("didAddPOpup !");
		jQuery("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
		win.close();
	}
}