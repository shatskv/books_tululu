from datetime import datetime, timedelta
from books.models import Book, Author, Genre, BookProgress
import pytest
from random import randint
from django.contrib.auth.models import User
import os
from glob import glob


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test__Book_model__create(iteration, datetime_now, random_text, rating, year, image_file, text_file, delete_files_by_patern):
    book = Book.objects.create(
                        title=random_text, 
                        description=random_text, 
                        text=text_file,
                        cover=image_file,
                        rating=rating,
                        year_published=year,
    )
    image_name, img_ext = image_file.name.split('.')
    text_name, txt_ext = text_file.name.split('.')
    assert book.title == random_text
    assert text_name in str(book.text) and book.text.path.split('.')[1] == txt_ext
    assert image_name in str(book.cover) and book.cover.path.split('.')[1] == img_ext 
    assert book.description == random_text
    assert book.year_published == year
    assert book.rating == rating
    assert book.created_at + timedelta(hours=1) > datetime_now 
    assert book.updated_at + timedelta(hours=1) > datetime_now
    assert f'Book {random_text} year: {year}, rating: {rating}' == str(book)

    delete_files_by_patern(image_file, book.cover.path)
    delete_files_by_patern(text_file, book.text.path)


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test__Author_model__create(iteration, random_text, birthdate):
    author = Author.objects.create(fullname=random_text, birthdate=birthdate)

    assert author.fullname == random_text
    assert author.birthdate == birthdate
    assert str(author) == f'{random_text} birtdate: {birthdate}'


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test__Genre_model__create(iteration, random_text):
    genre = Genre.objects.create(name=random_text)

    assert genre.name == random_text
    assert str(genre) == random_text


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test__Book_model__author_foreign_key(iteration, author_obj, random_text):
    author = author_obj()
    book = Book.objects.create(
                        title=random_text,
                        author=author, 
    )

    assert book.author == author


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test_Book_model_genres_many_to_many(iteration,  genre_obj, random_text):
    genre_one = genre_obj
    genre_two = genre_obj
    book = Book.objects.create(
                        title=random_text,
    )
    book.genres.set([genre_one, genre_two])
    assert book in genre_one.books.all()


@pytest.mark.django_db
@pytest.mark.parametrize('iteration', range(10))
def test_BookProgress_model_foreigns_key(iteration, random_text):
    book = Book.objects.create(title=random_text)
    user = User.objects.create(username=random_text, password=random_text)
    book_progress = BookProgress(book=book, user=user, page=5, num_pages=10)

    assert book_progress.book == book
    assert book_progress.user == user


@pytest.mark.django_db
@pytest.mark.parametrize('page', range(11))
def test_BookProgress_model_str_and_progress(page,  genre_obj, random_text):
    book = Book.objects.create(title=random_text)
    user = User.objects.create(username=random_text, password=random_text)
    book_progress = BookProgress(book=book, user=user, page=page, num_pages=10)
    percentage = round(page / 10 * 100)
    assert book_progress.progress == percentage
    assert str(book_progress) == f'Book {random_text} are reading by {random_text}, progress {percentage}'
