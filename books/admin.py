from django.contrib import admin

from .models import Author, Book, Genre, BookProgress

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(BookProgress)
