
if(typeof jQuery.fn.autocompletehtml != 'function') {

(function($) {

$.fn.autocompletehtml = function() {
	var $text = $(this), sizeul = true;
	this.data("ui-autocomplete")._renderItem = function _renderItemHTML(ul, item) {
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
                var name = $(this).attr("name")

		var $text = $("<input type='text' value='' class='ui-autocomplete-input' autocomplete='off' role='textbox' aria-autocomplete='list' aria-haspopup='true' />")
		var $input = $('<input type="hidden"/>')
		var $deck = $('<div class="results_on_deck"></div>')

                $this
                    .removeAttr("id")
                    .removeAttr("name")

                $text
                    .attr("id", id+"_text")
                    .attr("name", name+"_text")

                $input
                    .attr("id", id)
                    .attr("name", name)

                $this
                    .prepend($input)
                    .prepend($deck)
                    .prepend($text)

		function receiveResult(event, ui) {
			if ($input.val()) {
				kill();
			}
			$input.val(ui.item.pk);
			$text.val('');
			addKiller(ui.item.repr);
			$text.trigger("added", [ui.item.pk,ui.item.repr]);

			return false;
		}

		function addKiller(repr,pk) {
			killButton = $('<span class="ui-icon ui-icon-trash">X</span> ');
                        $("<div></div>")
                            .attr("id", id+'_on_deck_'+pk)
                            .append(killButton)
                            .append(repr)
                            .appendTo($deck)
			killButton.click(function() {
				kill();
				$text.trigger("killed", [pk,repr]);
			});
		}

		function kill() {
			$input.val('');
			$deck.children().fadeOut(1.0).remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();

		if (options.initial) {
			its = options.initial;
                        $input.attr("value", its[1])
			addKiller(its[0], its[1]);
		}

		$this.bind('didAddPopup', function(event, pk, repr) {
			ui = { item: { pk: pk, repr: repr } }
			receiveResult(null, ui);
		});
	});
};

$.fn.autocompleteselectmultiple = function(options) {
	return this.each(function() {
		var id = this.id;

		var $this = $(this);
                var name = $(this).attr("name")

		var $text = $("<input type='text' value='' class='ui-autocomplete-input' autocomplete='off' role='textbox' aria-autocomplete='list' aria-haspopup='true' />")
		var $input = $('<input type="hidden"/>')
		var $deck = $('<div class="results_on_deck"></div>')

                $this
                    .removeAttr("id")
                    .removeAttr("name")

                $text
                    .attr("id", id+"_text")
                    .attr("name", name+"_text")

                $input
                    .attr("id", id)
                    .attr("name", name)

                $this
                    .prepend($input)
                    .prepend($deck)
                    .prepend($text)


		function receiveResult(event, ui) {
			pk = ui.item.pk;
			prev = $input.val();

			if (prev.indexOf("|"+pk+"|") == -1) {
				$input.val((prev ? prev : "|") + pk + "|");
				addKiller(ui.item.repr, pk);
				$text.val('');
				$text.trigger("added",  [pk,ui.item.repr]);
			}

			return false;
		}

		function addKiller(repr, pk) {
			var killButton = $('<span class="ui-icon ui-icon-trash">X</span> ');
                        $("<div></div>")
                            .attr("id", id+'_on_deck_'+pk)
                            .append(killButton)
                            .append(repr)
                            .appendTo($deck)
			killButton.click(function() {
				kill(pk);
				$text.trigger("killed", [pk,repr]);
			});
		}

		function kill(pk) {
			$input.val($this.val().replace("|" + pk + "|", "|"));
			$("#"+id+"_on_deck_"+pk).fadeOut().remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();

		if (options.initial) {
                        if (options.initial.length > 0) {
                            var value = $.map(options.initial, function(its){ return its[1] });
                            $input.attr("value", "|" + value.join("|") + "|")
                        } else {
                            $input.attr("value", "|")
                        }
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
