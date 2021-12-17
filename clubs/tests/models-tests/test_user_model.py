from django.test import TestCase
from clubs.models import User, Club

class UserModelTestCase(TestCase):
    """ Tests for showing a specific user profile """

    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/officer_user.json',
                'clubs/tests/fixtures/default_club.json']

    def setUp(self):
        self.john = User.objects.get(username='@johndoe')
        self.jane = User.objects.get(username='@janedoe')
        self.club = Club.objects.get(club_name = "Big chess")
        self.club.addMember(self.jane)

    def test_join_club(self):
        self.assertFalse(self.club.is_member(self.john))
        self.club.addMember(self.john)
        self.assertTrue(self.club.is_member(self.john))

    def test_promote_to_officer(self):
        self.assertFalse(self.club.is_officer(self.john))
        self.club.addOfficer(self.john)
        self.assertTrue(self.club.is_officer(self.john))

    def test_remove_from_club(self):
        self.assertTrue(self.club.is_member(self.jane))
        self.club.removeMember(self.jane)
        self.assertFalse(self.club.is_member(self.jane))

    def test_demote_officer(self):
        self.assertTrue(self.club.is_officer(self.jane))
        self.club.removeOfficer(self.jane)
        self.assertFalse(self.club.is_officer(self.jane))

    def test_remove_non_member_user_from_club(self):
        self.assertFalse(self.club.is_member(self.john))
        self.club.removeMember(self.john)
        self.assertFalse(self.club.is_member(self.john))

    def test_demote_non_officer_user(self):
        self.assertFalse(self.club.is_officer(self.john))
        self.club.removeOfficer(self.john)
        self.assertFalse(self.club.is_officer(self.john))

    def test_is_owner_for_real_owner(self):
        self.assertTrue(self.club.is_owner(self.jane))

    def test_is_owner_for_non_owner(self):
        self.assertFalse(self.club.is_owner(self.john))

    def test_add_member_that_is_already_member(self):
        self.assertTrue(self.club.is_member(self.jane))
        self.club.addMember(self.jane)
        self.assertTrue(self.club.is_member(self.jane))

    def test_promote_member_that_is_already_officer(self):
        self.assertTrue(self.club.is_officer(self.jane))
        self.club.addOfficer(self.jane)
        self.assertTrue(self.club.is_officer(self.jane))

    def test_return_correct_club_memberships(self):
        pass
