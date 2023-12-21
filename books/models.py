from datetime import date, timedelta
from random import randint, randrange, uniform

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


MIN_DATE = date(1800, 1, 1)
MAX_DATE = date(1980, 1, 1)


def generate_birhdate():
    days_between = (MAX_DATE - MIN_DATE).days
    random_number_of_days = randrange(days_between)
    random_date = MIN_DATE + timedelta(days=random_number_of_days)

    return random_date


class Author(models.Model):
    fullname = models.CharField(max_length=256, unique=True, db_index=True)
    birthdate = models.DateField(null=True, blank=True, default=generate_birhdate())

    def __str__(self):
        return f'{self.fullname} birtdate: {self.birthdate}'


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True,  blank=True)
    text = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=randint(30, 100)/10)
    genre = models.ManyToManyField(Genre)
    year_published = models.PositiveSmallIntegerField(validators=[MinValueValidator(MIN_DATE.year), 
                                                                     MaxValueValidator(MAX_DATE.year)],
                                                         default=randint(MIN_DATE.year, MAX_DATE.year))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Book {self.title} year: {self.year_published}, rating: {self.rating}'
