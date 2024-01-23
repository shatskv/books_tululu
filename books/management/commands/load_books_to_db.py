import json
import os
from datetime import date, datetime, timedelta
from random import randint
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from typing import Any
from books.management.commands.get_books_from_tululu import JSON_PATH
from books.models import Book, Author, Genre


# JSON_PATH = 'books.json'
MIN_DATE = date(1800, 1, 1)
MAX_DATE = date(1980, 1, 1)

class Command(BaseCommand):
    help = 'Скачивает книги с сайта'
    def handle(self, *args: Any, **options: Any) -> None:
        load_books()


def normalize_fullname(author: str) -> str:
    fullname_parts = author.strip().split()
    fullname_parts = [part.strip().capitalize() for part in fullname_parts]
    return ' '.join(fullname_parts)

def generate_birhdate_and_year_published():
    fake = Faker()
    # days_between = (MAX_DATE - MIN_DATE).days
    # random_number_of_days = randrange(days_between)
    # birhdate = MIN_DATE + timedelta(days=random_number_of_days)
    birhdate = fake.date_between(start_date=MIN_DATE, end_date=MAX_DATE)
    date_published = birhdate + timedelta(days=365*randint(20, 50))
    year_published = min(date_published, datetime.now().date()).year
    return birhdate, year_published


def load_books():

    json_path = os.path.join(settings.BOOKS_DIR, JSON_PATH)
    with open(json_path, 'r') as file:
        books_json = json.load(file)

    for book in books_json:
        title = book.get('title')
        author_name = book.get('author')
        description = book.get('description')
        img_src = book.get('img_src')
        book_path = book.get('book_path')
        genre_names = book.get('genres')
        author_name = normalize_fullname(author_name)
        image_name = os.path.basename(img_src)
        text_name = os.path.basename(book_path)
        rating = randint(30, 100) / 10
        birtdate, year = generate_birhdate_and_year_published()

        author = Author.objects.get_or_create(fullname=author_name)[0]
        author.birthdate = birtdate
        author.save()
        genres = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in genre_names]
        
        with open(img_src, 'rb') as img_file, open(book_path, 'rb') as txt_file:
            book_obj = Book.objects.get_or_create(
                title=title,
                author=author,
                description=description,
                cover=File(img_file, image_name),
                text=File(txt_file, text_name),
                year_published=year,
                rating=rating
            )[0]
            book_obj.genres.set(genres)
