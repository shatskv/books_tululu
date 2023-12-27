from django import forms

from .models import Author, Book, Genre


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'text', 'cover', 'genres', 'year_published']
        labels = {
            'title': 'Название',
            'author': 'Автор',
            'description': 'Описание',
            'text': 'Файл книги',
            'cover': 'Обложка',
            'genres': 'Жанры',
            'year_published': 'Год публикации'
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
