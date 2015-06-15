from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .sites import site


class SimpleAjaxSelectConfig(AppConfig):

    name = 'ajax_select'
    verbose_name = _('AjaxSelects')

    def ready(self):
        try:
            site.register(settings.AJAX_LOOKUP_CHANNELS)
        except AttributeError:
            raise ImproperlyConfigured("settings.AJAX_LOOKUP_CHANNELS is not configured")

class AjaxSelectConfig(SimpleAjaxSelectConfig):

    def ready(self):
        super(AjaxSelectConfig, self).ready()
        self.module.autodiscover()
