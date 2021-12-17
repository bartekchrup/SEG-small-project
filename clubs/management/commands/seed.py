from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club
import random
#from clubs.models import Club

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def _create_user(self):
        user = User.objects.create_user(
            username= "@"+self.faker.user_name(),

            first_name= self.faker.first_name(),
            last_name= self.faker.last_name(),
            experienceLevel = random.randint(1,5),
            personalStatement = self.faker.sentence(),
            bio=self.faker.text(),
            email=self.faker.unique.free_email(),
            password="Password123",

        )
        user.save()
        return user

    def createMembership(self, user, club, level):
        membership = Membership(
           user = user,
           club = club,
           level = level
        )
        membership.save()

    def createClub(self, owner):
        club = Club(
            owner=owner,
            name=self.faker.user_name() + " Chess club",
            location=self.faker.address(),
            description=self.faker.sentence()
        )
        club.save()
        return club

    def handle(self, *args, **options):
        jebadiah_user= User.objects.create_user(username = "@Jeb", first_name = "Jebadiah" , last_name = "", bio = "a", email = "jeb@example.org", experienceLevel = random.randint(1,5))
        valentina_user = User.objects.create_user(username = "@Val", first_name = "Valentina" , last_name = "Kerman", bio = "b", email = "val@example.org", experienceLevel = random.randint(1,5))
        billie_user= User.objects.create_user(username = "@Bil", first_name = "Billie" , last_name = "Kerman", bio = "c", email = "billie@example.org", experienceLevel = random.randint(1,5))
        kerbal_owner= User.objects.create_user(username = "@Kerba", first_name = "llama" , last_name = "SEG_Owner", bio = "d", email = "llama@example.org", experienceLevel = random.randint(1,5))
        kerbal_club=Club(
            owner=kerbal_owner,
            club_name="Kerbal Chess Club",
            location=self.faker.address(),
            description="This is Kerbal club."
        )
        kerbal_club.save()


        self.createMembership(jebediah_user, kerbal_club, '2')
        kerbal_club.members.add(jebediah_user)
        self.createMembership(valentina_user, kerbal_club, '2')
        kerbal_club.members.add(valentina_user)
        self.createMembership(billie_user, kerbal_club, '2')
        kerbal_club.members.add(billie_user)


        for i in range(5):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = first_name.lower() + last_name.lower() + "@owners.org"
            owner = None
            if(i != 1):
                owner = self._create_user()
            else:
                owner=valentina_user

            club = self.createClub(owner)

            if(i == 0):
                self.createMembership(jebediah_user, club, '3')
                club.members.add(jebediah_user)
            if(i == 2):
                self.createMembership(billie_user,club,'2')
                club.members.add(billie_user)

            for i in range(8):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = first_name.lower() + last_name.lower() + "@applicants.org"
                applicant = self._create_user()
                self.createMembership(applicant, club, "1")
                club.members.add(applicant)

            for i in range(10):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = first_name.lower() + last_name.lower() + "@members.org"
                member = self._create_user()
                self.createMembership(member, club, "2")
                club.members.add(member)

            for i in range(5):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = first_name.lower() + last_name.lower() + "@officers.org"
                officer = self._create_user()
                self.createMembership(officer, club, "3")
                club.members.add(officer)
    print("Users and Clubs Seeded")