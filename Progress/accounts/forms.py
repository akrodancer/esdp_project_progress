from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'password1', 'password2',
            'email',
            'phone',
        ]
    
    widgets = {
        'username' : forms.TextInput(attrs={'placeholder': 'Логин'}),
        'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        'phone': forms.TextInput(attrs={'placeholder': '+996 (XXX)-XX-XX'}),
    }