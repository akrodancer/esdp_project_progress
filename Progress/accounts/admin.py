from django.contrib import admin
from accounts.models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'phone'
    ]