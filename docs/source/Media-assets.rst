Media Assets
============

If `jQuery` or `jQuery.ui` are not already loaded on the page, then these will be loaded from CDN::

    ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js
    code.jquery.com/ui/1.10.3/jquery-ui.js
    code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css

If you want to prevent this and load your own then set::

    # settings.py
    AJAX_SELECT_BOOTSTRAP  = False


Customizing the style sheet
---------------------------

By default `css/ajax_select.css` is included by the Widget's media. This specifies a simple basic style.

If you would prefer not to have `css/ajax_select.css` loaded at all then you can implement your own `yourapp/static/ajax_select/css/ajax_select.css` and put your app before `ajax_select` in `INSTALLED_APPS`.

Your version will take precedence and Django will serve your `css/ajax_select.css`

The markup is simple and you can just add more css to override unwanted styles.

The trashcan icon comes from the jQueryUI theme by the css classes::

    "ui-icon ui-icon-trash"

The following css declaration::

    .results_on_deck .ui-icon.ui-icon-trash { }

would be "stronger" than jQuery's style declaration and thus you could make trash look less trashy.

The loading indicator is in `ajax_select/static/ajax_select/images/loading-indicator.gif`

`yourapp/static/ajax_select/images/loading-indicator.gif` would override that.
