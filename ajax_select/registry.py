from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


class LookupChannelRegistry(object):

    """
    Registry for lookup channels activated for your django project ("site").

    This includes any installed apps that contain lookup.py modules (django 1.7+)
    and any lookups that are explicitly declared in settings.AJAX_LOOKUP_CHANNELS
    """
    _registry = {}

    def load_channels(self):
        self._registry = {}
        try:
            from django.utils.module_loading import autodiscover_modules
        except ImportError:
            pass
        else:
            autodiscover_modules('lookups')

        if hasattr(settings, 'AJAX_LOOKUP_CHANNELS'):
            self.register(settings.AJAX_LOOKUP_CHANNELS)

    def register(self, lookup_specs):
        """
        lookup_specs is a dict with one or more LookupChannel specifications
        {'channel': ('module.of.lookups', 'MyLookupClass')}
        {'channel': {'model': 'MyModelToBeLookedUp', 'search_field': 'field_to_search'}}
        """
        for label, spec in lookup_specs.items():
            if spec is None:  # unset
                if label in self._registry:
                    del self._registry[label]
            else:
                self._registry[label] = spec

    def get(self, channel):
        """
        Find the LookupChannel for the named channel.

        @param channel {string} - name that the lookup channel was registered at
        """
        from lookup_channel import LookupChannel

        try:
            lookup_spec = self._registry[channel]
        except KeyError:
            raise ImproperlyConfigured(
                "No ajax_select LookupChannel named %(channel)r is registered." % {'channel': channel})

        if (type(lookup_spec) is type) and issubclass(lookup_spec, LookupChannel):
            return lookup_spec()
        elif isinstance(lookup_spec, dict):
            # 'channel' : dict(model='app.model', search_field='title' )
            #  generate a simple channel dynamically
            return self.make_channel(lookup_spec['model'], lookup_spec['search_field'])
        else:
            # a tuple
            # 'channel' : ('app.module','LookupClass')
            #  from app.module load LookupClass and instantiate
            lookup_module = __import__(lookup_spec[0], {}, {}, [''])
            lookup_class = getattr(lookup_module, lookup_spec[1])

            return lookup_class()

    def is_registered(self, channel):
        return channel in self._registry

    def make_channel(self, app_model, arg_search_field):
        """
        app_model:   app_name.ModelName
        arg_search_field:  the field to search against and to display in search results
        """
        from lookup_channel import LookupChannel
        app_label, model_name = app_model.split(".")

        class MadeLookupChannel(LookupChannel):

            model = get_model(app_label, model_name)
            search_field = arg_search_field

        return MadeLookupChannel()


registry = LookupChannelRegistry()


def get_model(app_label, model_name):
    """
    Get the model from 'app_label' 'ModelName'
    """
    try:
        # django >= 1.7
        from django.apps import apps
    except ImportError:
        # django < 1.7
        from django.db import models
        return models.get_model(app_label, model_name)
    else:
        return apps.get_model(app_label, model_name)


def can_autodiscover():
    try:
        from django.apps import AppConfig  # noqa
    except ImportError:
        return False
    return True


def register(channel):
    """
    Decorator to register a LookupClass


    ```
    from ajax_select import LookupChannel, register

    @register('agent')
    class AgentLookup(LookupClass):

        def get_query(self)
        def format_item(self)
        ... etc
    ```
    """

    def _wrapper(lookup_class):
        if not label:
            raise ValueError('Lookup Channel must have a channel name')

        registry.register({label: lookup_class})

        return lookup_class

    return _wrapper
