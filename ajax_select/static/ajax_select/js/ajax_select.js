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
      // TODO:this is suboptimal, make this a simple loop over the results from $(...)
      // TODO:WTF is the use of this?
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
      if ($.isArray(this.options.source)) {
        this.source = function(request, response) {
          response(filter(this.options.source, request.term));
        };
      } else if (typeof this.options.source == 'string') {
        // make source a function that will fetch new results the
        // first time it gets called and reset the current scroll 
        // state accordingly.

        var self = this;
        // flag that prevents us from binding the scroll event
        // handler multiple times
        self.isMenuScrollEventBound = false;
        this.source = function(request, response) {
          // abort existing request when available
          if (self.xhr) {
            self.xhr.abort();
          }

          // initialize offset
          self._offset = 0;
          // end of file marker in case that subsequent requests
          // yield an empty result which will prevent us from making
          // redundant roundtrips to the server
          self._eof = false;

          // use sensible defaults if non were provided
          if (typeof self.options.limit == 'undefined') {
            self.options.limit = 3;
          }

          request.offset = self._offset;
          request.limit = self.options.limit;
          self._requestIncrementally(request, response);
        }
      }
      else {
        throw new Error('source must be either an array or a url');
      }
    },
    // Adapted from http://jsfiddle.net/LesignButure/EVsye/
    _renderMenu: function (ul, items) {

      var self = this;
      $.each(items, function (index, item) {
        self._renderItemData(ul, item);
      });
      if (!$.isArray(this.options.source)) {
        var $ul = $(ul);

        if (!self.isMenuScrollEventBound) {
          self.isMenuScrollEventBound = true;
          $ul.scroll(function () {

            function isScrollbarBottom(container) {
              var height = container.outerHeight();
              var scrollHeight = container[0].scrollHeight;
              var scrollTop = container.scrollTop();

              return scrollTop >= scrollHeight - height;
            };

            // prevent this from querying the server if no more results are available
            if (!self._eof && isScrollbarBottom($ul)) {

              self._addSpinner(ul);
              self._requestIncrementally({term:self.term, offset:self._offset, limit:self._limit}, function (results) {

                self._removeSpinner(ul);
                if (results.length == 0) {
                  self.data('eof', true);
                }
                else {
                  // render items
                  $.each(results, function (index, item) {
                    self._renderItemData(ul, item);
                  });

                  // refresh menu
                  self.menu.deactivate();
                  self.menu.refresh();
                  // size and position menu
                  $ul.show();
                  self._resizeMenu();
                  $ul.position($.extend({
                    of: self.element
                  }, self.options.position));
                  if (self.options.autoFocus) {
                    self.menu.next(new $.Event("mouseover"));
                  }
                }
              });
            }
          });
        }
      }
    },
    _addSpinner: function(ul) {
      // TODO:implement
    },
    _removeSpinner: function(ul) {
      // TODO:implement
    },
    _requestIncrementally: function(request, response) {

      var self = this;
      this.xhr = $.ajax({
        url : self.options.source,
        type : self.options.method,
        data : request,
        dataFilter : function (data, type) {
          // we assume that the result is a valid json array
          return $.parseJSON(data);
        },
        success : function (data, textStatus, jqXHR) {
          if (data.length < self.options.limit) {
            self._eof = true;
          }
          // update current offset
          self._offset += data.length;
          response(data);
        },
        error : function (jqXHR, textStatus, errorThrown) {
          // TODO:error handling
          // For now we will simply mimic the original behaviour
          response([]);
        }
      });
    },
    _renderItem: function(ul, item) {
      var body = this.options.html ? item.match: item.label;
      return $('<li>')
        .append($('<a>')[this.options.html ? 'html' : 'text' ](body))
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

    // TODO:eats some performance each time any of these are clicked - really necessary?
    $('.inline-group ul.tools a.add, .inline-group div.add-row a, .inline-group .tabular tr.add-row td a').on('click', function() {
      $(window).trigger('init-autocomplete');
    });
  });

})(window.jQuery);
