from books.views.books import books_view, book_view, home_view, authors_view, genres_view, books_by_author_view, books_by_genre_view
import pytest
from django.urls import reverse


def test__book_view__successfully(db, client, user, create_book):
    client.force_login(user)
    book = create_book
    url = reverse('books', kwargs={'book_id': book.pk})
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.description in content
    assert str(book.year_published) in content
    assert book.author.fullname in content


def test__book_view__redirect(db, client, create_book):
    # client.force_login(user=user)
    book = create_book
    url = reverse('books', kwargs={'book_id': book.pk})
    response = client.get(url)

    assert response.status_code == 302


def test__books_view__successfully(db, client, user, create_book):
    client.force_login(user)
    book = create_book
    url = reverse('all_books')
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.author.fullname in content


def test__books_view__redirect(db, client, create_book):
    create_book
    url = reverse('all_books')
    response = client.get(url)

    assert response.status_code == 302


def test__home_view__redirect(client):
    response = client.get('/')

    assert response.status_code == 302


def test__genres_view__successfully(db, client, create_book):
    book = create_book
    response = client.get('/genres/')

    content = response.content.decode()

    assert response.status_code == 200
    for genre in book.genres.all():
        assert genre.name in content


def test__authors_view__successfully(db, client, create_book):
    book = create_book
    response = client.get('/authors/')

    content = response.content.decode()

    assert response.status_code == 200
    assert book.author.fullname in content


def test__books_by_author_view__successfully(db, client, user, create_book):
    client.force_login(user)
    book = create_book
    url = reverse('authors', kwargs={'author_id': book.author.pk})
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.author.fullname in content


def test__books_by_author_view__redirect(db, client, create_book):
    book = create_book
    url = reverse('authors', kwargs={'author_id': book.author.pk})
    response = client.get(url)

    assert response.status_code == 302


def test__books_by_genre_view__successfully(db, client, user, create_book):
    client.force_login(user)
    book = create_book
    url = reverse('genres', kwargs={'genre_id': book.genres.all()[0].pk})
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.genres.all()[0].name in content


def test__books_by_genre_view__redirect(db, client, create_book):
    book = create_book
    url = reverse('genres', kwargs={'genre_id': book.genres.all()[0].pk})
    response = client.get(url)

    assert response.status_code == 302
