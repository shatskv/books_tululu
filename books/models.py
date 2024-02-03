

from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=256,  unique=True, db_index=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.fullname} birtdate: {self.birthdate}'


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,  blank=True, related_name='books')
    description = models.TextField(max_length=5000, null=True, blank=True)
    text = models.FileField(upload_to='texts/', null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=0)
    genres = models.ManyToManyField(Genre, related_name='books')
    year_published = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Book {self.title} year: {self.year_published}, rating: {self.rating}'


class BookProgress(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_books')
    page = models.PositiveIntegerField(null=True, blank=True)
    num_pages = models.PositiveIntegerField(null=True, blank=True)


    @property
    def progress(self) -> float:
        percentage = 0
        if self.page is not None and self.num_pages is not None:
            book_progress = self.page / self.num_pages if self.num_pages else 0
            percentage = round(book_progress * 100)
        return percentage


    def __str__(self) -> str:
        return f'Book {self.book.title} are reading by {self.user.username}, progress {self.progress}'
