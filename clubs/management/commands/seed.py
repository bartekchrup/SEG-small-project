from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from ...models import User

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def _create_user(self):
        user = User.objects.create_user(
            "@"+self.faker.user_name(),
            first_name= self.faker.first_name(),
            last_name= self.faker.last_name(),
            bio=self.faker.text(),
            email=self.faker.unique.free_email(),
            password= self.faker.password(),
        )
        user.save()

    def handle(self, *args, **options):
         
        for _ in range(100):
            self._create_user()

        print('Seed user ')
