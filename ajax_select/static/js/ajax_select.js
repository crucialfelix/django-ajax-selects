

if(typeof jQuery.fn.autocompletehtml != 'function') {

(function($) {

function _renderItemHTML(ul, item) {
	return $("<li></li>")
		.data("item.autocomplete", item)
		.append("<a>" + item.match + "</a>")
		.appendTo(ul);
}

$.fn.autocompletehtml = function() {
	this.data("autocomplete")._renderItem = _renderItemHTML;
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
			addKiller(ui.item.repr);
			$deck.trigger("added");

			return false;
		}

		function addKiller(repr,pk) {
			killer_id = "kill_" + pk + id;
			killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
			if (repr) {
				$deck.empty();
				$deck.append("<div>" + killButton + repr + "</div>");
			} else {
				$("#"+id+"_on_deck > div").prepend(killButton);
			}
			$("#" + killer_id).click(function() {
				kill();
				$deck.trigger("killed");
			});
		}

		function kill() {
			$this.val('');
			$deck.children().fadeOut(1.0).remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();

		$deck.position({
			my: "right top",
			at: "right bottom",
			of: $text,
			offset: "0 15"
		});

		if (options.initial) {
			its = options.initial;
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
		var $text = $("#"+id+"_text");
		var $deck = $("#"+id+"_on_deck");

		function receiveResult(event, ui) {
			pk = ui.item.pk;
			prev = $this.val();
			
			if (prev.indexOf("|"+pk+"|") == -1) {
				$this.val((prev ? prev : "|") + pk + "|");
				addKiller(ui.item.repr, pk);
				$text.val('');
				$deck.trigger("added");
			}

			return false;
		}

		function addKiller(repr, pk) {
			killer_id = "kill_" + pk + id;
			killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
			$deck.append('<div id="'+id+'_on_deck_'+pk+'">' + killButton + repr + ' </div>');

			$("#"+killer_id).click(function() {
				kill(pk);
				$deck.trigger("killed");
			});
		}

		function kill(pk) {
			$this.val($this.val().replace("|" + pk + "|", "|"));
			$("#"+id+"_on_deck_"+pk).fadeOut().remove();
		}

		options.select = receiveResult;
		$text.autocomplete(options);
		$text.autocompletehtml();
		$deck.position({
			my: "right top",
			at: "right bottom",
			of: $text,
			offset: "0 15"
		});
		
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
})(jQuery);

/* 	the popup handler
	requires RelatedObjects.js which is part of the django admin js
	so if using outside of the admin then you would need to include that manually */
	function didAddPopup(win,newId,newRepr) {
		var name = windowname_to_id(win.name);
		jQuery("#"+name).trigger('didAddPopup',[html_unescape(newId),html_unescape(newRepr)]);
		win.close();
	}
}