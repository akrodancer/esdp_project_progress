from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


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


class LoginUserForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget = forms.PasswordInput, validators=[validate_password])
           
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = get_user_model().user_set.by_username(username)

        if not user:
            raise forms.ValidationError('User not found!')
        elif not check_password(password, user.password):
            raise forms.ValidationError('Incorrect password!')
        else:
            return self.cleaned_data
            
        




class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
