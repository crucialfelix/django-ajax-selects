from django.apps import AppConfig


class AjaxSelectConfig(AppConfig):

    """
    Django 1.7+ enables initializing installed applications
    and autodiscovering modules

    On startup, search for and import any modules called `lookups.py` in all installed apps.
    Your LookupClass subclass may register itself.
    """

    name = 'ajax_select'
    verbose_name = 'Ajax Selects'

    def ready(self):
        from django.conf import settings
        from ajax_select.registry import registry
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules('lookups')

        if hasattr(settings, 'AJAX_LOOKUP_CHANNELS'):
            registry.register(settings.AJAX_LOOKUP_CHANNELS)
