"""Tests of the log out view"""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club

class LogOutViewTestCase(TestCase):
    """Tests of the log out view"""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/officer_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.john = User.objects.get(username='@johndoe')
        self.jane = User.objects.get(username='@janedoe')
        self.club = Club.objects.get(club_name = "Big chess")

    def test_change_to_valid_selected_club(self):
        self.client.login(username=self.jane.username, password='Password123')
        url = reverse('switch_club', kwargs={'club_id': self.club.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(User.objects.get(username='@janedoe').preferredClub, self.club)
