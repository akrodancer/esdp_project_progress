from django.contrib import admin
from accounts.models import User, Comment, SignedUpUsers


class CommentsInline(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = ('teacher', 'content', 'created_at')
    fk_name = 'student'


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]
    list_filter = [
        "is_staff",
    ]
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
        'get_role_display',
        'is_staff'
    )
    fields = ('username', 'first_name', 'last_name', 
              'avatar', 'email', 'phone', 'role')


@admin.register(SignedUpUsers)
class SignedUpUsersAdmin(admin.ModelAdmin):
    list_display = ('first_name',
                    'last_name',
                    'phone',
                    'email',
                    'course')
    readonly_fields = ('first_name', 
                       'last_name',
                       'phone',
                       'email',
    )