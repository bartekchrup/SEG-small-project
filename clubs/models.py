from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from libgravatar import Gravatar

class User(AbstractUser):
    """User model used for authentication and club authoring."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    is_applicant = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_officer = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    class Experience(models.TextChoices):
        EXPERT = 'Expert'
        ADVANCED = 'Advanced'
        INTERMEDIATE = 'Intermediate'
        BEGINER = 'Beginer'
    experienceLevel = models.CharField(max_length=20, choices=Experience.choices, default = "BEGINER")
    personalStatement = models.CharField(max_length=200, blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        return self.gravatar(size=60)

class Club(models.Model):
    club_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    club_name = models.CharField(max_length = 50, unique = True, blank = False)
    club_location = models.CharField(max_length = 100, unique = False, blank = False)
    club_description = models.CharField(max_length = 520, blank = True)
