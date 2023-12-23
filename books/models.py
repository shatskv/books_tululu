

from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=256, unique=True, db_index=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.fullname} birtdate: {self.birthdate}'


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,  blank=True)
    text = models.FileField(upload_to='texts/', null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    year_published = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Book {self.title} year: {self.year_published}, rating: {self.rating}'
