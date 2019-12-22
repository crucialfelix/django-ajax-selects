from django.contrib.auth.models import User
from django.test import TestCase

from tests.lookups import PersonWithTitleLookup, UserLookup
from tests.models import PersonWithTitle


class TestLookups(TestCase):

    def test_get_objects(self):
        user1 = User.objects.create(username='user1',
                                    email='user1@example.com',
                                    password='password')
        user2 = User.objects.create(username='user2',
                                    email='user2@example.com',
                                    password='password')
        lookup = UserLookup()
        # deliberately asking for them backwards:
        users = lookup.get_objects([user2.id, user1.id])
        self.assertEqual(len(users), 2)
        # to make sure they come back in the order requested
        u2, u1 = users
        self.assertEqual(u1, user1)
        self.assertEqual(u2, user2)

    def test_get_objects_inherited_model(self):
        """
        Tests that get_objects works with inherited models
        """
        one = PersonWithTitle.objects.create(name='one', title='The One')
        two = PersonWithTitle.objects.create(name='two', title='The Other')
        lookup = PersonWithTitleLookup()
        users = lookup.get_objects([one.id, two.id])
        self.assertEqual(len(users), 2)
        u1, u2 = users
        self.assertEqual(u1, one)
        self.assertEqual(u2, two)
