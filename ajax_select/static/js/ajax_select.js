if (typeof jQuery == 'undefined') {
    try { // use django admins
        jQuery=django.jQuery;
    } catch(err) {
        document.write('<script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"><\/script>');
    }
}
if(typeof jQuery == 'undefined' || (typeof jQuery.ui == 'undefined')) {
    document.write('<script type="text/javascript"  src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js"><\/script>');
    document.write('<link type="text/css" rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/smoothness/jquery-ui.css" />');
}
//]]>

if(typeof jQuery.fn.autocompletehtml != 'function') {

(function($) {

$.fn.autocompletehtml = function() {
	var $text = $(this), sizeul = true;
	this.data("autocomplete")._renderItem = function _renderItemHTML(ul, item) {
		if(sizeul) {
			if(ul.css('max-width')=='none') ul.css('max-width',$text.outerWidth());
			sizeul = false;
		}
		return $("<li></li>")
			.data("item.autocomplete", item)
			.append("<a>" + item.match + "</a>")
			.appendTo(ul);
	};
	return this;
}
$.fn.autocompleteselect = function(options) {

	return this.each(function() {
		var id = this.id;
		var $this = $(this);

		var $text = $("#"+id+"_text");
		var $deck = $("#"+id+"_on_deck");

		function receiveResult(event, ui) {
			if ($this.val()) {
				kill();
			}
			$this.val(ui.item.pk);
			$text.val('');
			addKiller(ui.item.repr, null, ui.item.url);
			$deck.trigger("added");
			$this.change();
			return false;
		}

		function addKiller(repr, pk, url) {
			killer_id = "kill_" + pk + id;
			killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
			if (repr) {
				$deck.empty();
				if (url){
					repr = '<a href="' + url + '" target="_blank">' + repr + '</a>';
				}
				$deck.append("<div>" + killButton + repr + "</div>");
			} else {
				$("#"+id+"_on_deck > div").prepend(killButton);
			}
			$("#" + killer_id).click(function() {
				if (options.confirm_text){
					var delete_item = confirm(options.confirm_text);
					if (delete_item) {
						kill();
						$deck.trigger("killed");
					}
				} else {
					kill();
					$deck.trigger("killed");
				}
			});
		}

		function kill() {
			$this.val('');
			$this.change();
			$deck.children().fadeOut(1.0).remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();

		if (options.initial) {
			its = options.initial;
			addKiller(its[0], its[1]);
		}

		$this.bind('didAddPopup', function(event, pk, repr) {
			ui = { item: { pk: pk, repr: repr } };
			receiveResult(null, ui);
		});

		$this.change(function (ev) {
			var pk, repr, ui;
			if (typeof ev.cloneSource !== 'undefined') {
				pk = ev.cloneSource.val();
				// depends on addKiller implementation
				repr = ev.cloneSource.next().children('div').children().slice(1);
				repr = $.map(repr, function (el) {
					return el.outerHTML;
				}).join('');
				ui = { item: { pk: pk, repr: repr } };
				receiveResult(null, ui);
			}
		});
	});
};

$.fn.autocompleteselectmultiple = function(options) {
	return this.each(function() {
		var id = this.id;

		var $this = $(this);
		var $text = $("#"+id+"_text");
		var $deck = $("#"+id+"_on_deck");

		function receiveResult(event, ui) {
			pk = ui.item.pk;
			prev = $this.val();

			if (prev.indexOf("|"+pk+"|") == -1) {
				$this.val((prev ? prev : "|") + pk + "|");
				addKiller(ui.item.repr, pk, ui.item.url);
				$text.val('');
				$deck.trigger("added");
				$this.change();
			}

			return false;
		}

		function addKiller(repr, pk, url) {
			killer_id = "kill_" + pk + id;
			killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
			var item_content = null;
			if (url) {
				item_content = '<div id="'+ id +'_on_deck_' + pk + '">' +
					killButton + '<a href="' + url + '" target="_blank">' + repr + '</a></div>';
			} else {
				item_content = '<div id="'+id+'_on_deck_'+pk+'">' + killButton + repr + ' </div>';
			}
			$deck.append(item_content);

			$("#"+killer_id).click(function() {
				if (options.confirm_text){
					var delete_item = confirm(options.confirm_text);
					if (delete_item) {
						kill(pk);
						$deck.trigger("killed");
					}
				} else {
					kill(pk);
					$deck.trigger("killed");
				}
			});
		}

		function kill(pk) {
			$this.val($this.val().replace("|" + pk + "|", "|"));
			$("#"+id+"_on_deck_"+pk).fadeOut().remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();

		if (options.initial) {
			$.each(options.initial, function(i, its) {
				addKiller(its[0], its[1]);
			});
		}

		$this.bind('didAddPopup', function(event, pk, repr) {
			ui = { item: { pk: pk, repr: repr } }
			receiveResult(null, ui);
		});
	});
};

window.addAutoComplete = function (prefix_id, callback ) { /*(html_id)*/
	/* detects inline forms and converts the html_id if needed */
	var prefix = 0;
	var html_id = prefix_id;
	if(html_id.indexOf("__prefix__") != -1) {
		// Some dirty loop to find the appropriate element to apply the callback to
		while ($('#'+html_id).length) {
			html_id = prefix_id.replace(/__prefix__/, prefix++);
		}
		html_id = prefix_id.replace(/__prefix__/, prefix-2);
		// Ignore the first call to this function, the one that is triggered when
		// page is loaded just because the "empty" form is there.
		if ($("#"+html_id+", #"+html_id+"_text").hasClass("ui-autocomplete-input"))
			return;
	}
	callback(html_id);
}
/*	the popup handler
	requires RelatedObjects.js which is part of the django admin js
	so if using outside of the admin then you would need to include that manually */
window.didAddPopup = function (win,newId,newRepr) {
	var name = windowname_to_id(win.name);
	$("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
	win.close();
}

})(jQuery);

}


var BobAjaxSelect = (function (window, undefined) {
    'use strict';

    var instance;

    var BobAjaxSelectAPI = function () {}

    BobAjaxSelectAPI.prototype.register_text_field = function (selector, options) {
        addAutoComplete(selector, function(html_id) {
            options['select'] =
                function(event, ui) {
                    $("#"+html_id).val(ui.item.value).trigger("added");
                    return false;
                }
            $("#"+html_id).autocomplete(options).autocompletehtml();
        });
    }

    BobAjaxSelectAPI.prototype.register_select_field = function (selector, options) {
        addAutoComplete(selector, function(html_id) {
           $("#"+html_id).autocompleteselect(options);
        });
    }

    BobAjaxSelectAPI.prototype.register_selectmultiple_field = function (selector, options) {
        addAutoComplete(selector, function(html_id) {
           $("#"+html_id).autocompleteselectmultiple(options);
        });
    }

    BobAjaxSelectAPI.prototype._register_fields = function (type, selector, options) {
        var instance = BobAjaxSelect.getInstance();
        switch (type) {
            case 'text':
                instance.register_text_field(selector, options);
                break;
            case 'select':
                instance.register_select_field(selector, options);
                break;
            case 'selectmultiple':
                instance.register_selectmultiple_field(selector, options);
                break;
        }
    }

    BobAjaxSelectAPI.prototype.register_in_element = function (element) {
        var instance = BobAjaxSelect.getInstance();
        var text_fields = $(element).find('[data-bob-text-field-options]');
        var select_fields = $(element).find('[data-bob-select-field-options]');
        var selectmultiple_fields = $(element).find('[data-bob-selectmultiple-field-options]');
        var fields = {
            'text': text_fields,
            'select': select_fields,
            'selectmultiple': selectmultiple_fields,
        }

        $.each( fields, function( key, values ) {
            var data_name = 'bob-' + key + '-field-options';
            $.each( values, function( i, field ) {
                instance._register_fields(
                    key, field.id, $(field).data(data_name)
                );
            });
        });
    }


    BobAjaxSelectAPI.prototype.register_on_load = function () {
        var instance = BobAjaxSelect.getInstance();
        instance.register_in_element($('body'));
    }

    var getInstance = function () {
        if (!instance) {
            instance = new BobAjaxSelectAPI();
        }
        return instance;
    }

    return {
        getInstance: getInstance
    }

})(window);

$(document).ready(function() {
    bob_ajax_select_instance = BobAjaxSelect.getInstance();
    bob_ajax_select_instance.register_on_load();
});
