Lookup Channels
===============

A LookupChannel defines how to search and how to format found objects for display in the interface.

LookupChannels are registered with a "channel name" and fields refer to that name.

You may have only one LookupChannel for a model, or you might define several for the same Model each with different queries, security policies and formatting styles.

Custom templates can be created for channels. This enables adding extra javascript or custom UI. See :doc:`/Custom-Templates`


lookups.py
----------

Write your LookupChannel classes in a file name `yourapp/lookups.py`

(note: inside your app, not your top level project)

Use the @register decorator to register your LookupChannels by name

`example/lookups.py`::

    from ajax_select import register, LookupChannel

    @register('things')
    class ThingsLookup(LookupChannel):

        model = Things

        def get_query(self, q, request):
              return self.model.objects.filter(title__icontains=q).order_by('title')


If you are using Django >= 1.7 then all `lookups.py` in all of your apps will be automatically imported on startup.

If Django < 1.7 then you can import each of your lookups in your views or urls.
Or you can register them in settings (see below).

Customize
---------

.. automodule:: ajax_select.lookup_channel
  :members: LookupChannel
  :noindex:


settings.py
-----------

Versions previous to 1.4 loaded the LookupChannels according to `settings.AJAX_LOOKUP_CHANNELS`

This will still work.  Your LookupChannels will continue to load without having to add them with the new @register decorator.

Example::

    # settings.py

      AJAX_LOOKUP_CHANNELS = {
          # auto-create a channel named 'person' that searches by name on the model Person
          # str: dict
          'person': {'model': 'example.person', 'search_field': 'name'}

          # specify a lookup to be loaded
          # str: tuple
          'song': ('example.lookups', 'SongLookup'),

          # delete a lookup channel registered by an app/lookups.py
          # str: None
          'users': None
      }


One situation where it is still useful: if a resuable app defines a LookupChannel and you want to override that or turn it off.
Pass None as in the third example above.

Anything in `settings.AJAX_LOOKUP_CHANNELS` overwrites anything previously registered by an app.
