from django import forms
from accounts.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewUserForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'password1', 'password2',
            'email',
            'phone',
        ]
    
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'Логин'}),
            'first_name' : forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name' : forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+996 (XXX)-XX-XX'}),
        }


class LoginUserForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    class Meta:
        model = get_user_model()
        fields = [
            'username', 
            'password',
        ]
    
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'Логин'}),
        }



class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
