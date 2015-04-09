define(['jquery', 'mustache', 'jquery-ui'], function ($, Mustache) {
    'use strict';
    var instance, its;

    $.fn.autocompletehtml = function() {
        var $text = $(this), sizeul = true;
        this.data('uiAutocomplete')._renderItem = function _renderItemHTML(
            ul, item
        ) {
            if(sizeul) {
                if(ul.css('max-width')=='none') ul.css(
                    'max-width',$text.outerWidth()
                );
                sizeul = false;
            }
            return $('<li></li>')
                .data('item.autocomplete', item)
                .append('<a>' + item.match + '</a>')
                .appendTo(ul);
        };
        return this;
    };

    $.fn.autocompleteselect = function(options) {

        return this.each(function() {
            var id = this.id;
            var $this = $(this);

            var $text = $('#' + id + '_text');
            var $deck = $('#' + id + '_on_deck');

            function receiveResult(event, ui) {
                if ($this.val()) {
                    kill();
                }
                $this.val(ui.item.pk);
                $text.val('');
                addKiller(ui.item.repr, null, ui.item.url);
                $deck.trigger('added');
                $this.change();
                return false;
            }

            function addKiller(repr, pk, url) {
                var killer_id, killButton;
                killer_id = 'kill_' + pk + id;
                killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
                if (repr) {
                    $deck.empty();
                    if (url){
                        repr = '<a href="' + url + '" target="_blank">' + repr + '</a>';
                    }
                    $deck.append('<div>' + killButton + repr + '</div>');
                } else {
                    $('#'+id+'_on_deck > div').prepend(killButton);
                }
                $('#' + killer_id).click(function() {
                    if (options.confirm_text){
                        var delete_item = confirm(options.confirm_text);
                        if (delete_item) {
                            kill();
                            $deck.trigger('killed');
                        }
                    } else {
                        kill();
                        $deck.trigger('killed');
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
                var ui = {item: {pk: pk, repr: repr}};
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
            var $text = $('#' + id + '_text');
            var $deck = $('#' + id + '_on_deck');

            function receiveResult(event, ui) {
                var pk = ui.item.pk;
                var prev = $this.val();

                if (prev.indexOf('|'+pk+'|') == -1) {
                    $this.val((prev ? prev : '|') + pk + '|');
                    addKiller(ui.item.repr, pk, ui.item.url);
                    $text.val('');
                    $deck.trigger('added');
                    $this.change();
                }

                return false;
            }

            function addKiller(repr, pk, url) {
                var killer_id, killButton;
                killer_id = 'kill_' + pk + id;
                killButton = '<span class="ui-icon ui-icon-trash" id="'+killer_id+'">X</span> ';
                var item_content = null;
                if (url) {
                    item_content = '<div id="'+ id +'_on_deck_' + pk + '">' +
                        killButton + '<a href="' + url + '" target="_blank">' + repr + '</a></div>';
                } else {
                    item_content = '<div id="'+id+'_on_deck_'+pk+'">' + killButton + repr + ' </div>';
                }
                $deck.append(item_content);

                $('#'+killer_id).click(function() {
                    if (options.confirm_text){
                        var delete_item = confirm(options.confirm_text);
                        if (delete_item) {
                            kill(pk);
                            $deck.trigger('killed');
                        }
                    } else {
                        kill(pk);
                        $deck.trigger('killed');
                    }
                });
            }

            function kill(pk) {
                $this.val($this.val().replace('|' + pk + '|', '|'));
                $('#'+id+'_on_deck_'+pk).fadeOut().remove();
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
                var ui = {item: {pk: pk, repr: repr}};
                receiveResult(null, ui);
            });

            function resetWidget() {
                var allSelects = $this.parent().children('div');
                allSelects.slice(1).remove();
                $(allSelects[0]).children().remove();
                $this.val('|');
            }

            $this.change(function (ev) {
                if (typeof ev.cloneSource !== 'undefined') {
                    resetWidget();

                    var pk = ev.cloneSource.val();
                    var pks = pk.split('|').slice(1, -1);

                    var divs = ev.cloneSource.next().children('div');
                    $.each(divs, function(key, item) {
                        var repr = $(item).children('a').html();
                        pk = pks[key];
                        var ui = {
                            item: {
                                tabel: pk,
                                match: repr,
                                pk: pk,
                                repr: repr,
                                url: $(item).children('a').attr('href'),
                                value: pk
                            }
                        };
                        receiveResult(null, ui);
                    });
                }
            });
        });
    };

    window.addAutoComplete = function (prefix_id, callback ) { /*(html_id)*/
        /* detects inline forms and converts the html_id if needed */
        var prefix = 0;
        var html_id = prefix_id;
        if(html_id.indexOf('__prefix__') != -1) {
            // Some dirty loop to find the appropriate element to apply the callback to
            while ($('#' + html_id).length) {
                html_id = prefix_id.replace(/__prefix__/, prefix++);
            }
            html_id = prefix_id.replace(/__prefix__/, prefix-2);
            // Ignore the first call to this function, the one that is triggered when
            // page is loaded just because the "empty" form is there.
            if ($('#' + html_id + ', #' + html_id + '_text').hasClass('ui-autocomplete-input'))
                return;
        }
        callback(html_id);
    };
    /*    the popup handler
        requires RelatedObjects.js which is part of the django admin js so if
        using outside of the admin then you would need to include that
        manually
    */
    window.didAddPopup = function (win,newId,newRepr) {
        var name = windowname_to_id(win.name);
        $('#'+name).trigger('didAddPopup',[html_unescape(newId), html_unescape(newRepr)]);
        win.close();
    };

    var BobAjaxSelectAPI = function () {};

    BobAjaxSelectAPI.prototype.register_text_field = function (
        selector, options
    ) {
        addAutoComplete(selector, function(html_id) {
            options.select = function(event, ui) {
                $('#' + html_id).val(ui.item.value).trigger('added');
                return false;
            }
            $('#' + html_id).autocomplete(options).autocompletehtml();
        });
    };

    BobAjaxSelectAPI.prototype.register_select_field = function (
        selector, options
    ) {
        addAutoComplete(selector, function(html_id) {
           $('#' + html_id).autocompleteselect(options);
        });
    };

    BobAjaxSelectAPI.prototype.register_selectmultiple_field = function (
            selector, options
        ) {
        addAutoComplete(selector, function(html_id) {
           $('#' + html_id).autocompleteselectmultiple(options);
        });
    };

    BobAjaxSelectAPI.prototype._register_fields = function (
        type, selector, options
    ) {
        var instance = getInstance();
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
    };

    BobAjaxSelectAPI.prototype.register_in_element = function (element) {
        var instance = getInstance();
        var text_fields = $(element).find('[data-bob-text-field-options]');
        var select_fields = $(element).find('[data-bob-select-field-options]');
        var selectmultiple_fields = $(element).find('[data-bob-selectmultiple-field-options]');
        var fields = {
            'text': text_fields,
            'select': select_fields,
            'selectmultiple': selectmultiple_fields,
        };

        $.each( fields, function( key, values ) {
            var data_name = 'bob-' + key + '-field-options';
            $.each( values, function( i, field ) {
                instance._register_fields(
                    key, field.id, $(field).data(data_name)
                );
            });
        });

        // handler for AutoCompleteCascadeSelectField - in the future, it might be better
        // to convert it to one of those '$.fn.autocompleteselect...' functions
        (function () {
            // iterate over all child inputs having 'data-parent-id' as an attribute
            $('input[data-parent-id]').each(function (i, input) {
                var childId = input.id.substring(0, input.id.length - 5);
                var childHiddenSel = 'input[type=hidden]#' + childId;
                var parentDeck = $('#' + $(input).data('parentId') + '_on_deck');
                var childDeck = $('#' + childId + '_on_deck');
                // get the original AJAX source from options
                var options = $(input).data('uiAutocomplete').options;
                var source = options.source;
                // get the initial value that may be already selected on parent
                var parent = $('#' + $(input).data('parentId'));
                var pk = parseInt(parent.val(), 10) || void 0;
                // get/reset the pk's value from parent when it's added/removed
                parentDeck.on('added', function () {
                    pk = parseInt(parent.val(), 10) || void 0;
                });
                parentDeck.on('killed', function () {
                    pk = void 0;
                });
                // reset the value of the hidden child field when it's deck gets killed
                childDeck.on('killed', function () {
                    $(childHiddenSel).val('');
                });
                // modify the autocomplete function in a way that it apart the usual query
                // (term) it should also send the value selected in the parent field (pk)
                $(input).autocomplete('option', 'source', function(request, response) {
                    $.getJSON(source, {'term': request.term, 'parent_pk': pk}, response);
                });
            });
            // similar as above, but for CascadeModelChoiceField
            $('select[data-parent-id]').each(function (i, input) {
                var parentDeck = $('#' + $(input).data('parentId') + '_on_deck');
                var parent = $('#' + $(input).data('parentId'));
                var pk = parseInt(parent.val(), 10) || void 0;
                var source = $(input).attr('data-channel');
                var clearChoices = function (input) {
                    $(input).find('option').remove();
                    $(input).append($('<option></option>').val('').html('---------'));
                };
                var getChoices = function (input, pk, initial) {
                    var optionSelected = $(input).find('option[selected=selected]').val();
                    $.ajax({
                        'type': 'GET',
                        'url': source + '?term=' + pk,
                        'dataType': 'json',
                        'cache': false,
                        'success': function (json) {
                            clearChoices(input);
                            for (var i = 0; i < json.length; i++) {
                                $(input).append($('<option></option>').val(json[i].pk).html(json[i].value));
                            }
                            if (initial === true) {
                                $(input).find('option[value=' + optionSelected + ']').attr('selected', 'selected');
                            }
                        }
                    });
                };
                if(typeof pk === 'undefined'){
                    // clear possible child choices if parent is undefined (ex. on empty, initial form)
                    clearChoices(input);
                }
                else{
                    // initialization of available choices, hence 'true' as third argument
                    getChoices(input, pk, true);
                }
                if (parentDeck.length === 0) {
                    // parent field's widget is simple *select*
                    $('#' + $(input).data('parentId')).on('change', function () {
                        pk = parseInt(parent.val(), 10) || void 0;
                        getChoices(input, pk);
                    });
                } else {
                    // parent field's widget is *AutoCompleteSelectWidget*
                    parentDeck.on('added', function () {
                        pk = parseInt(parent.val(), 10) || void 0;
                        getChoices(input, pk);
                    });
                    parentDeck.on('killed', function () {
                        pk = void 0;
                        clearChoices(input);
                    });
                }
            });

        })();
    };


    BobAjaxSelectAPI.prototype.register_on_load = function () {
        var instance = getInstance();
        instance.register_in_element($('body'));
    };

    function getInstance  () {
        if (!instance) {
            instance = new BobAjaxSelectAPI();
        }
        return instance;
    }

    function initialize() {
        var bob_ajax_select_instance;
        bob_ajax_select_instance = getInstance();
        bob_ajax_select_instance.register_on_load();
    }

    return {
        getInstance: getInstance,
        initialize: initialize
    };
});
