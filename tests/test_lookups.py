
from django.test import TestCase
from django.contrib.auth.models import User
from .lookups import UserLookup


class TestLookups(TestCase):

    def test_get_objects(self):
        user1 = User.objects.create(username='user1',
            email='user1@example.com',
            password='password')
        user2 = User.objects.create(username='user2',
            email='user2@example.com',
            password='password')
        lookup = UserLookup()
        users = lookup.get_objects([user2.id, user1.id])
        self.assertEqual(len(users), 2)
        u2, u1 = users
        self.assertEqual(u1, user1)
        self.assertEqual(u2, user2)
