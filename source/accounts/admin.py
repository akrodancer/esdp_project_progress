from django.contrib import admin
from accounts.models import User, Comment, SignedUpUsers
from django.conf import settings


class CommentsInline(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = ('teacher', 'content', 'created_at')
    fk_name = 'student'

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]
    list_display = (
        'username',
        'email',
        'phone',
        'get_role_display'
    )
    fields = ('username', 'first_name', 'last_name', 
              'avatar', 'email', 'phone', 'role')


@admin.register(SignedUpUsers)
class SignedUpUsersAdmin(admin.ModelAdmin):
    list_display = ('first_name',
                    'last_name')
    readonly_fields = ('first_name', 
                       'last_name',
                       'phone',
                       'email',
    )