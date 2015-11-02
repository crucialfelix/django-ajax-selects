
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.core import urlresolvers


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin',
            email='email@example.com',
            password='password')
        self.client = Client()
        self.client.login(username='admin', password='password')

    def test_add_popup_get(self):
        app_label = 'tests'
        model = 'author'
        url = urlresolvers.reverse('add_popup', kwargs={
            'app_label': app_label,
            'model': model
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_popup_post(self):
        app_label = 'tests'
        model = 'author'
        url = urlresolvers.reverse('add_popup', kwargs={
            'app_label': app_label,
            'model': model
        })
        data = dict(name='Name')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        content = response.content.decode('UTF-8')

        self.assertFalse('dismissAddRelatedObjectPopup' in content)
        self.assertFalse('dismissAddAnotherPopup' in content)
        self.assertTrue('didAddPopup' in content)
