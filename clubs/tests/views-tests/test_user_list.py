from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club

class UserListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/officer_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.url = reverse('user_list')
        self.user = User.objects.get(username='@janedoe')
        self.club = Club.objects.get(club_name = "Big chess")
        self.user.preferredClub = self.club
        self.user.save()

    def test_user_list_url(self):
        self.assertEqual(self.url,'/users/')

    def test_get_user_list(self):
        users_to_add = 15 -1 #Jane doe is 1 user
        self._create_test_users(users_to_add)
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(users_to_add):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(username=f'@user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_users(self, user_count=10):
        for user_id in range(user_count):
            user = User.objects.create_user(f'@user{user_id}',
                email=f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
            )
            self.club.addMember(user)
