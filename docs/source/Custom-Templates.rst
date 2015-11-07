Customizing Templates
=====================

Each form field widget is rendered using a template:

- autocomplete.html
- autocompleteselect.html
- autocompleteselectmultiple.html

You may write a custom template for your channel:

- yourapp/templates/ajax_select/{channel}_autocomplete.html
- yourapp/templates/ajax_select/{channel}_autocompleteselect.html
- yourapp/templates/ajax_select/{channel}_autocompleteselectmultiple.html


And customize these blocks::

    {% block extra_script %}
    <script type="text/javascript">
        $("#{{html_id}}_on_deck").bind('added', function() {
          var id = $("#{{html_id}}").val();
          console.log('added id:' + id );
        });
        $("#{{html_id}}_on_deck").bind('killed', function() {
          var current = $("#{{html_id}}").val()
          console.log('removed, current is:' + current);
        });
    </script>
    {% endblock %}

    {% block help %}
    <p>
      You could put additional UI or help text here.
    </p>
    {% endblock %}
