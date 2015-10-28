
class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class AjaxSelectSite(object):

    def __init__(self):
        self._registry = {}

    def register(self, lookup_labels):
        # channel data structure is { 'channel' : ( module.lookup, lookupclass ) }
        # or                        { 'channel' : { 'model': 'xxxxx', 'search_field': 'xxxx' }}
        self._registry.update(lookup_labels)

    def unregister(self, lookup_labels):
        """
        Unregisters the given model(s).
        If a model isn't already registered, this will raise NotRegistered.
        """
        # channel data structure is { label : ( module.lookup, lookupclass ) }
        for channel_name in lookup_labels.keys():
            if not self.is_registered(channel_name):
                raise NotRegistered('The channel "%s" is not registered' % channel_name)
            del self._registry[channel_name]

    def is_registered(self, label):
        """
        Check if a LookupChannel class is registered with this `AjaxSelectSite`.
        """
        return label in self._registry


site = AjaxSelectSite()
