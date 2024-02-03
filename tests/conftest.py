import os
from datetime import date, datetime, timedelta, timezone
from glob import glob
from random import randint

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from books.models import Author, Book, BookProgress, Genre


@pytest.fixture
def min_date():
    return date(1800, 1, 1)


@pytest.fixture
def max_date():
    return date(1980, 1, 1)


@pytest.fixture
def datetime_now():
    return datetime.now(timezone.utc)


@pytest.fixture
def rating():
    return randint(30, 100) / 10


@pytest.fixture
def random_text():
    fake = Faker(['ru-RU'])
    return fake.pystr()


@pytest.fixture
def birthdate(min_date, max_date):
    fake = Faker(['ru-RU'])
    birhdate = fake.date_between(start_date=min_date, end_date=max_date)
    return birhdate


@pytest.fixture
def year():
    return randint(1800, 1980)


@pytest.fixture
def genre_obj():
    fake = Faker(['ru-RU'])
    genre = Genre.objects.create(name=fake.pystr())

    return genre


@pytest.fixture
def list_genre_obj_pk(genre_obj):
    def inner():
        genres = [genre_obj.pk for _ in range(randint(2, 4))]
        return genres
    return inner


@pytest.fixture
def author_obj(random_text, birthdate):
    def inner():
        author = Author.objects.create(fullname=random_text, birthdate=birthdate)
        return author
    return inner


# @pytest.fixture
# def create_book():
#     def inner(title=None, 
#               description=None, 
#               text=None,
#               cover=None,
#               rating=None,
#               year_published=None,
#               created_at=None,
#               updated_at=None
#             ):
#         book = Book(title=title, 
#                     description=description, 
#                     text=text,
#                     cover=cover,
#                     rating=rating,
#                     year_published=year_published,
#                     created_at=created_at,
#                     updated_at=updated_at)
#         return book
#     return inner

@pytest.fixture
def create_book(author_obj, genre_obj, random_text, year):
    book = Book.objects.create(title=random_text,
                               description=random_text,
                               author=author_obj(),
                               year_published=year,
                               rating=6.0)
    
    book.genres.set([genre_obj, genre_obj])
    return book
    

@pytest.fixture
def get_fixture_value(request):
    def inner(fixture_name):
        try:
            obj = request.getfixturevalue(fixture_name)
        except pytest.FixtureLookupError:
            obj = fixture_name
        return obj
    return inner


@pytest.fixture
def delete_files_by_patern():
    def inner(base_file, filepath):
        directory_path = os.path.dirname(filepath)
        file_name, file_ext = base_file.name.split('.')
        for file in glob(f'{directory_path}/{file_name}*.{file_ext}'):
            os.remove(file)
    return inner


@pytest.fixture
def image_file():
    file = SimpleUploadedFile(name='test_cover.jpg', content=b'', content_type='image/jpeg')
    return file


@pytest.fixture
def text_file():
    return SimpleUploadedFile(name='test_text.txt', content=b'Sample text', content_type='text/plain')


@pytest.fixture
def user(random_text):
    user = User.objects.create(username=random_text, password=random_text)
    return user


@pytest.fixture
def moderator(random_text):
    user = User.objects.create(username=random_text, password=random_text, is_staff=True)
    return user

@pytest.fixture
def book_progress(user, create_book):
    book = create_book
    book_progress = BookProgress.objects.create(book=book, user=user)
    return book_progress
