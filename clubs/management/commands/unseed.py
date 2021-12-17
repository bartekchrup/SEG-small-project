from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from clubs.models import User, Club

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print('Deleting all users ')
        for user in User.objects.all():
            if not user.is_superuser:
                user.delete()
        print('Deleting all Clubs')
        Club.objects.all().delete()