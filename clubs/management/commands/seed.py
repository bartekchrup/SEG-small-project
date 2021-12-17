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
            "@"+self.faker.user_name(),
            first_name= self.faker.first_name(),
            last_name= self.faker.last_name(),
            experienceLevel = random.randint(1,5),
            personalStatement = self.faker.sentence(),
            bio=self.faker.text(),
            email=self.faker.unique.free_email(),
            password= self.faker.password(),

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
        jebediah_user=self.create_user("Jebediah","Kerman","jeb@example.org")
        valentina_user=self.create_user("Valentina","Kerman","val@example.org")
        billie_user=self.create_user("Billie","Kerman","billie@example.org")
        kerbal_owner=self.create_user('Gemsbok', 'SEG_Owner', 'gemsbok@owners.org')
        kerbal_club=Club(
            owner=kerbal_owner,
            name="Kerbal Chess Club",
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
                owner = self.create_user(first_name, last_name, username)
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
                applicant = self.create_user(first_name, last_name, username)
                self.createMembership(applicant, club, "1")
                club.members.add(applicant)

            for i in range(10):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = first_name.lower() + last_name.lower() + "@members.org"
                member = self.create_user(first_name, last_name, username)
                self.createMembership(member, club, "2")
                club.members.add(member)

            for i in range(5):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                username = first_name.lower() + last_name.lower() + "@officers.org"
                officer = self.create_user(first_name, last_name, username)
                self.createMembership(officer, club, "3")
                club.members.add(officer)
    print("Users and Clubs Seeded")