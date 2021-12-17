from django.test import TestCase
from clubs.models import User, Club
from django.core.exceptions import ValidationError

class ClubModelTestCase(TestCase):
    """ Tests for showing a club profile """

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username = '@johndoe')
        self.club = Club.objects.get(club_name = 'ClubOne')
        self.club = Club.objects.get(club_location = 'Location')
        self.club = Club.objects.get(club_description = 'Description')


    def club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()


    #Tests for the club_location

    def test_club_name_is_not_blank(self):
        self.club.club_name = ''
        self.club_is_invalid()

    def test_club_name_is_unique(self):
        another_club = Club.objects.get(club_name = 'ClubTwo')
        self.club.club_name != another_club.club_name
        self.club_is_invalid()

    def test_club_name_has_numbers(self):
        self.club.club_name = "Club1"
        self.club_is_valid()

    def test_club_name_has_space_characters(self):
        self.club.club_name = "Club 1"
        self.club_is_valid()

    def test_club_name_has_less_than_50_characters(self):
        self.club.club_name = 'x' * 50
        self.club_is_valid()

    def test_club_name_has_more_than_50_characters(self):
        self.club.club_name = 'x' * 51
        self.club_is_invalid()


    #Tests for the club_location

    def test_club_location_is_not_blank(self):
        self.club.location = ''
        self.club_is_invalid()

    def test_club_location_is_not_unique(self):
        another_club = Club.objects.get(club_location = "Location")
        self.club.club_location = second_club.club_location
        self.club_is_valid()

    def test_club_location_has_less_than_100_characters(self):
        self.club.club_location = 'x' * 100
        self.club_is_valid()

    def test_club_location_has_more_than_100_characters(self):
        self.club.club_location = 'x' * 101
        self.club_is_invalid()


    #Tests for the club_description

    def test_club_description_can_be_blank(self):
        self.club.club_description = ''
        self.club_is_valid()

    def test_club_description_is_not_unique(self):
        second_club = Club.objects.get(club_description = "Description")
        self.club.club_description = second_club.club_description
        self.club_is_valid()

    def test_club_description_has_less_than_520_charecters(self):
        self.club.club_description = 'x' * 520
        self.club_is_valid()

    def test_description_has_more_than_520_charecters(self):
        self.club.club_description = 'x' * 521
        self.club_is_invalid()
