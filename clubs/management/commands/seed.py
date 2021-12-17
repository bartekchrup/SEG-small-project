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

    def createClub(self, owner):
        club = Club(
            owner=owner,
            club_name=self.faker.user_name() + " Chess club",
            club_location=self.faker.address(),
            club_description=self.faker.sentence()
        )
        club.save()
        return club

    def handle(self, *args, **options):
        jebadiah_user= User.objects.create_user(username = "@Jeb", first_name = "Jebadiah" , last_name = "", bio = "a", email = "jeb@example.org", experienceLevel = random.randint(1,5))
        valentina_user = User.objects.create_user(username = "@Val", first_name = "Valentina" , last_name = "Kerman", bio = "b", email = "val@example.org", experienceLevel = random.randint(1,5))
        billie_user= User.objects.create_user(username = "@Bil", first_name = "Billie" , last_name = "Kerman", bio = "c", email = "billie@example.org", experienceLevel = random.randint(1,5))
        kerbal_owner= User.objects.create_user(username = "@BillieKerban", first_name = "llama" , last_name = "SEG_Owner", bio = "d", email = "llama2@example.org", experienceLevel = random.randint(1,5))
        kerbal_club=Club(
            owner=kerbal_owner,
            club_name="Kerbal Chess Club",
            club_location=self.faker.address(),
            club_description="This is Kerbal club."
        )
        kerbal_club.save()
        kerbal_club.members.add(jebadiah_user)
        kerbal_club.officers.add(valentina_user)
        kerbal_club.owner = billie_user
        kerbal_club.save()

        for i in range(5):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = first_name.lower() + last_name.lower() + "@owners.org"
            owner = None
            if(i != 2):
                owner = self._create_user()
            else:
                owner = valentina_user
            
            if(i == 1):
                club.officers.add(jebadiah_user)

            if(i == 3):
                club.members.add(billie_user)
            
            club = self.createClub(owner)
            
            for i in range(8):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                email = first_name.lower() + last_name.lower() + "@applicants.org"
                applicant = self._create_user() 
                club.members.add(applicant)

            for i in range(10):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                email = first_name.lower() + last_name.lower() + "@members.org"
                member = self._create_user()  
                club.members.add(member)

            for i in range(5):
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                email = first_name.lower() + last_name.lower() + "@officers.org"
                officer = self._create_user()
                club.members.add(officer)
    print("Users and Clubs Seeded")