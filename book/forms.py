from django import forms
from django.contrib.auth import authenticate

from .models import Book, Reviews
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#DataFlair
class BookCreate(forms.ModelForm):

	class Meta:
		model = Book
		fields = '__all__'


class ReviewForm(forms.ModelForm):

	class Meta:
		model = Reviews
		fields = {"name", "text"}


class SignUpForm(UserCreationForm):
	city = forms.CharField()

	class Meta:
		model = User
		fields = ('username', 'city', 'password1', 'password2', )


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
