from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club
from clubs.tests.helpers import reverse_with_next


class ApplicantsTestCase(TestCase):
    """Tests of the applicants"""

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/officer_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.john = User.objects.get(username='@johndoe')
        self.club = Club.objects.get(club_name = "Big chess")
        self.url = reverse('join_club', kwargs={'club_id': self.club.id})

    def test_applicants_when_not_login_in(self):
        self.club.addApplicants(self.john)
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code = 302, target_status_code = 404)
