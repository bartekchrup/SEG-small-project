from django.contrib import admin
from clubs.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
     list_display = [
      'username', 'first_name', 'last_name', 'email', 'is_active',
     ]