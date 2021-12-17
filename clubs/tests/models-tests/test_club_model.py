from django.test import TestCase
from clubs.models import User, Club

class ClubModelTestCase(TestCase):
    """ Tests for showing a club profile """

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='@johndoe')
