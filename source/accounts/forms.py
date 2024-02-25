from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class NewUserForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
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


class LoginUserForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    class Meta:
        model = User
        fields = [
            'username', 
            'password',
        ]
    
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder': 'Логин'}),
        }



class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
