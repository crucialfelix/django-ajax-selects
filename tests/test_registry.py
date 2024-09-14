from django.test import TestCase

import ajax_select


class TestRegistry(TestCase):
    def test_lookup_py_is_autoloaded(self):
        """Django >= 1.7 autoloads tests/lookups.py."""
        is_registered = ajax_select.registry.is_registered("person")
        self.assertTrue(is_registered)

    def test_back_compatible_loads_by_settings(self):
        """A module and class specified in settings."""
        self.assertTrue(ajax_select.registry.is_registered("book"))

    def test_autoconstruct_from_spec(self):
        """A dict in settings specifying model and lookup fields."""
        self.assertTrue(ajax_select.registry.is_registered("author"))

    def test_unsetting_a_channel(self):
        """Settings can unset a channel that was specified in a lookups.py."""
        # self.assertFalse(ajax_select.registry.is_registered('user'))
        self.assertFalse(ajax_select.registry.is_registered("was-never-a-channel"))
