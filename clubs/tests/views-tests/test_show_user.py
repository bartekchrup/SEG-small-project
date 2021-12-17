from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club

class ShowUserTest(TestCase):
    """ Tests for showing a specific user profile """

    fixtures = ['clubs/tests/fixtures/officer_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.user = User.objects.get(username='@janedoe')
        self.club = Club.objects.get(club_name = "Big chess")
        self.user.preferredClub = self.club
        self.user.save()
        self.url = reverse('show_user', kwargs={'user_id': self.user.id}) + f'?club={self.club.id}'

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.user.id}?club={self.club.id}')

    def test_get_show_user_as_owner(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'owner_show_user.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "@janedoe")


    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')
