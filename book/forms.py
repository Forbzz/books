import logging

from django import forms
from django.contrib.auth import authenticate
from .models import Book, Reviews, User, Profile
from django.contrib.auth.forms import UserCreationForm


# DataFlair
class BookCreate (forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class ProfileEditForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class UserRegistrationForm (forms.ModelForm):
    password = forms.CharField (label = 'Пароль', widget = forms.PasswordInput)
    password2 = forms.CharField (label = 'Повторите пароль', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2 (self):
        logger = logging.getLogger('django')
        cd = self.cleaned_data
        if cd ['password'] != cd ['password2']:
            logger.info('Password are different')
            raise forms.ValidationError ('Passwords don\'t match.')
        logger.info('Passwords are the same')
        return cd ['password2']


class ReviewForm (forms.ModelForm):
    class Meta:
        model = Reviews
        fields = {"name", "text"}


class SignUpForm (UserCreationForm):
    email = forms.EmailField (max_length = 255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
