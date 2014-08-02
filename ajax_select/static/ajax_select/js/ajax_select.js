'use strict';

(function ($) {

  $.fn.autocompleteselect = function (options) {
    return this.each(function () {
      var id = this.id,
          $this = $(this),
          $text = $('#' + id + '_text'),
          $deck = $('#' + id + '_on_deck');

      function receiveResult(event, ui) {
        if ($this.val()) {
          kill();
        }
        $this.val(ui.item.pk);
        $text.val('');
        addKiller(ui.item.repr, ui.item.pk);
        $deck.trigger('added', [ui.item.pk, ui.item]);
        $this.trigger('change');

        return false;
      }

      function addKiller(repr, pk) {
        var killer_id = 'kill_' + pk + id,
            killButton = '<span class="ui-icon ui-icon-trash" id="' + killer_id + '">X</span> ';
        if (repr) {
          $deck.empty();
          $deck.append('<div>' + killButton + repr + '</div>');
        } else {
          $('#' + id+'_on_deck > div').prepend(killButton);
        }
        $('#' + killer_id).click(function () {
          kill();
          $deck.trigger('killed', [pk]);
        });
      }

      function kill() {
        $this.val('');
        $deck.children().fadeOut(1.0).remove();
      }

      options.select = receiveResult;
      $text.autocomplete(options);

      if (options.initial) {
        addKiller(options.initial[0], options.initial[1]);
      }

      $this.bind('didAddPopup', function (event, pk, repr) {
        receiveResult(null, {item: {pk: pk, repr: repr}});
      });
    });
  };

  $.fn.autocompleteselectmultiple = function (options) {
    return this.each(function () {
      var id = this.id,
          $this = $(this),
          $text = $('#' + id+'_text'),
          $deck = $('#' + id+'_on_deck');

      function receiveResult(event, ui) {
        var pk = ui.item.pk,
            prev = $this.val();

        if (prev.indexOf('|'+pk+'|') === -1) {
          $this.val((prev ? prev : '|') + pk + '|');
          addKiller(ui.item.repr, pk);
          $text.val('');
          $deck.trigger('added', [ui.item.pk, ui.item]);
          $this.trigger('change');
        }
        return false;
      }

      function addKiller(repr, pk) {
        var killer_id = 'kill_' + pk + id,
            killButton = '<span class="ui-icon ui-icon-trash" id="' + killer_id + '">X</span> ';
        $deck.append('<div id="' + id + '_on_deck_' + pk + '">' + killButton + repr + ' </div>');

        $('#' + killer_id).click(function () {
          kill(pk);
          $deck.trigger('killed', [pk]);
        });
      }

      function kill(pk) {
        $this.val($this.val().replace('|' + pk + '|', '|'));
        $('#' + id+'_on_deck_'+pk).fadeOut().remove();
      }

      options.select = receiveResult;
      $text.autocomplete(options);

      if (options.initial) {
        $.each(options.initial, function (i, its) {
          addKiller(its[0], its[1]);
        });
      }

      $this.bind('didAddPopup', function (event, pk, repr) {
        receiveResult(null, {item: {pk: pk, repr: repr }});
      });
    });
  };

  function addAutoComplete (inp, callback) {
    var $inp = $(inp),
        html_id = inp.id,
        prefix_id = html_id,
        opts = JSON.parse($inp.attr('data-plugin-options')),
        prefix = 0;

    /* detects inline forms and converts the html_id if needed */
    if (html_id.indexOf('__prefix__') !== -1) {
      // Some dirty loop to find the appropriate element to apply the callback to
      while ($('#' + html_id).length) {
        html_id = prefix_id.replace(/__prefix__/, prefix++);
      }
      html_id = prefix_id.replace(/__prefix__/, prefix - 2);
      // Ignore the first call to this function, the one that is triggered when
      // page is loaded just because the 'empty' form is there.
      if ($('#' + html_id + ', #' + html_id + '_text').hasClass('ui-autocomplete-input')) {
        return;
      }
    }

    callback($inp, opts);
  }

  // allow html in the results menu
  // https://github.com/scottgonzalez/jquery-ui-extensions
  var proto = $.ui.autocomplete.prototype,
      initSource = proto._initSource;

  function filter(array, term) {
    var matcher = new RegExp($.ui.autocomplete.escapeRegex(term), 'i');
    return $.grep(array, function(value) {
      return matcher.test($('<div>').html(value.label || value.value || value).text());
    });
  }

  $.extend(proto, {
    _initSource: function() {
      if (this.options.html && $.isArray(this.options.source)) {
        this.source = function(request, response) {
          response(filter(this.options.source, request.term));
        };
      } else {
        initSource.call(this);
      }
    },
    _renderItem: function(ul, item) {
      var body = this.options.html ? item.match: item.label;
      return $('<li></li>')
        .data('item.autocomplete', item)
        .append($('<a></a>')[this.options.html ? 'html' : 'text' ](body))
        .appendTo(ul);
    }
  });

  /*  the popup handler
    requires RelatedObjects.js which is part of the django admin js
    so if using outside of the admin then you would need to include that manually */
  window.didAddPopup = function (win, newId, newRepr) {
    var name = window.windowname_to_id(win.name);
    $('#' + name).trigger('didAddPopup', [window.html_unescape(newId), window.html_unescape(newRepr)]);
    win.close();
  };

  // activate any on page
  $(window).bind('init-autocomplete', function () {

    $('input[data-ajax-select=autocomplete]').each(function (i, inp) {
      addAutoComplete(inp, function ($inp, opts) {
        opts.select =
            function (event, ui) {
              $inp.val(ui.item.value).trigger('added', [ui.item.pk, ui.item]);
              return false;
            };
        $inp.autocomplete(opts);
      });
    });

    $('input[data-ajax-select=autocompleteselect]').each(function (i, inp) {
      addAutoComplete(inp, function ($inp, opts) {
        $inp.autocompleteselect(opts);
      });
    });

    $('input[data-ajax-select=autocompleteselectmultiple]').each(function (i, inp) {
      addAutoComplete(inp, function ($inp, opts) {
        $inp.autocompleteselectmultiple(opts);
      });
    });

  });

  $(document).ready(function () {
    // if dynamically injecting forms onto a page
    // you can trigger them to be ajax-selects-ified:
    $(window).trigger('init-autocomplete');
    $('.inline-group ul.tools a.add, .inline-group div.add-row a, .inline-group .tabular tr.add-row td a').on('click', function() {
      $(window).trigger('init-autocomplete');
    });
  });

})(window.jQuery);
