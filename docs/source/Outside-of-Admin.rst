Outside of the Admin
====================

ajax_selects does not need to be in a Django admin.

When placing your form on the page be sure to include the static assets:

    {{ form.media }}

This includes the javascript and css files.

If you need to support "Add.."" popups then note that the popups will still use an admin view (the registered admin for the model being added), even if the form from where the popup was launched does not.

In your view, after creating your ModelForm object::

    autoselect_fields_check_can_add(form, model, request.user)

This will check each widget and enable the green + for them iff the User has permission.
