from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model


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
    password = forms.CharField(label='password',)
           
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Error')
        elif password != get_user_model().objects.get(username=username).password:
            raise forms.ValidationError('Error')
        else:
            return self.cleaned_data
            
        




class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
