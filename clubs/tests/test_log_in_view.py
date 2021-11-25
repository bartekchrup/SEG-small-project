"""Tests of the log in view"""
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm

class LogInViewTestCase(TestCase):
    """Tests of the log in view"""

    def setUp(self):
        self.url = reverse('log_in')

    def test_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
