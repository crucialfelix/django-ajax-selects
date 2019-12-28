from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin',
                                                  email='email@example.com',
                                                  password='password')
        self.client = Client()
        self.client.login(username='admin', password='password')
