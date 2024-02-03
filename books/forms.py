from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Author, Book, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'text', 'cover', 'genres', 'year_published']
        labels = {
            'title': 'Название:',
            'author': 'Автор:',
            'description': 'Описание:',
            'text': 'Файл книги:',
            'cover': 'Обложка:',
            'genres': 'Жанры:',
            'year_published': 'Год публикации:'
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'birthdate']
        labels = {
            'fullname': 'Имя автора',
            'birthdate': 'Дата рождения',
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': 'Название жанра'
            }


class SearchForm(forms.Form):
    title = forms.CharField(max_length=256, required=False)
    author = forms.CharField(max_length=256, required=False)
    description = forms.CharField(max_length=5000, required=False)
    genre = forms.CharField(max_length=256, required=False)
    rating_to = forms.FloatField(min_value=0, max_value=10, required=False, help_text='0.0')
    rating_from = forms.FloatField(min_value=0, max_value=10, required=False,)
