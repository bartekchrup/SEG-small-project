from django.contrib import admin
from clubs.models import User, Club
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
     ]

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = [
        'club_name', 'club_location', 'club_description'
    ]
