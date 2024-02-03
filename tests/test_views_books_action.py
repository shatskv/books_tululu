from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from  urllib.parse import urlencode
import pytest
from books.models import Book


def test__update_book_view__not_staff_user(db, user, client, create_book):
    book = create_book
    client.force_login(user)
    url = reverse('update_book', kwargs={'book_id': book.pk})
    
    response = client.get(url)
    assert response.status_code == 302


def test__update_book_view__get_staff_user(db, moderator, client, create_book):
    book = create_book
    client.force_login(moderator)
    url = reverse('update_book', kwargs={'book_id': book.pk})

    response = client.get(url)
    
    assert response.status_code == 200


def test__update_book_view__post_staff_user(db, moderator, client, create_book, delete_files_by_patern, text_file):
    book = create_book
    client.force_login(moderator)
    url = reverse('update_book', kwargs={'book_id': book.pk})
    book_data = {
        'title': 'new',
        'author': book.author.pk,
        'description': 'Описание',
        'text': text_file,
        'genres': book.genres.all()[0].pk,
        'year_published': 1950,
    }

    response = client.post(url, book_data, follow=True)
    content = response.content.decode()
    book.refresh_from_db()

    assert response.status_code == 200
    assert book_data['title'] in content
    assert book_data['description'] in content
    assert str(book_data['year_published']) in content
    assert book.title == book_data['title']
    assert book.description == book_data['description']
    assert book.year_published == book_data['year_published']

    delete_files_by_patern(text_file, book.text.path)


def test__search_view__no_books(db, create_book, user, client):
    create_book
    client.force_login(user)

    url = reverse('search')
    response = client.post(url, {'search_field': 'dsdfdfsfd'}, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert 'По вашему запросу ничего не найдено' in content


def test__search_view__no_search_value_redirect(db, create_book, user, client):
    book = create_book
    client.force_login(user)

    url = reverse('search')
    response = client.post(url, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content


def test__search_view__search_title_book(db, create_book, user, client):
    book = create_book
    client.force_login(user)

    url = reverse('search')
    response = client.post(url, {'search_field': book.title}, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content


def test__search_view__search_title_author(db, create_book, user, client):
    book = create_book
    client.force_login(user)

    url = reverse('search')
    response = client.post(url, {'search_field': book.author.fullname}, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content


def test__reader_view__no_text(db, create_book, user, client):
    book = create_book
    client.force_login(user)

    url = reverse('reader', kwargs={'book_id': book.pk})
    response = client.get(url)

    content = response.content.decode()

    assert response.status_code == 200
    assert 'Текст книги не найден!' in content, content


def test__reader_view__text(db, create_book, user, client, text_file, delete_files_by_patern):
    book = create_book
    book.text = text_file
    book.save()
    with open(book.text.path, 'r') as file:
            text = file.read()

    client.force_login(user)

    url = reverse('reader', kwargs={'book_id': book.pk})
    response = client.get(url)


    content = response.content.decode()

    assert response.status_code == 200
    assert  text in content

    delete_files_by_patern(text_file, book.text.path)


def test__search_details_view__books_found_title(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'title': book.title,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content


def test__search_details_view__books_found_author(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'author': book.author.fullname,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content


def test__search_details_view__books_found_genre(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'genre': book.genres.all()[0],
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content


def test__search_details_view__books_found_genre(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'description': book.description,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content

def test__search_details_view__books_found_rating_to(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'rating_to': 9.0,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content


def test__search_details_view__books_found_rating_from(db, client, create_book, user):
    book = create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'rating_from': 6.0,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert book.title in content
    assert book.genres.all()[0].name in content
    assert book.author.fullname in content


def test__search_details_view__books_not_found(db, client, create_book, user):
    create_book
    url = reverse('search_details')
    client.force_login(user)

    book_data = {
        'rating_from': 9.9,
    }

    response = client.post(url, book_data, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert 'По вашему запросу ничего не найдено' in content


def test__create_book_view__redirect_normal_user(db, client, user):
    client.force_login(user)
    url = reverse('new_book')

    response = client.get(url)

    assert response.status_code == 302


def test__create_book_view__get_staff_user(db, client, moderator):
    client.force_login(moderator)
    url = reverse('new_book')

    response = client.get(url)

    assert response.status_code == 200


def test__create_book_view__redirect_normal_user(db, client, moderator):
    client.force_login(moderator)
    url = reverse('new_book')

    response = client.get(url)

    assert response.status_code == 200


def test__create_book_view__post_staff_user(db, moderator, client, create_book, delete_files_by_patern, text_file):
    book = create_book
    client.force_login(moderator)
    url = reverse('new_book')
    book_data = {
        'title': 'new',
        'author': book.author.pk,
        'description': 'Описание',
        'text': text_file,
        'genres': book.genres.all()[0].pk,
        'year_published': 1950,
    }

    response = client.post(url, book_data, follow=True)
    content = response.content.decode()
    

    assert response.status_code == 200
    assert book_data['title'] in content
    assert book_data['description'] in content
    assert str(book_data['year_published']) in content
    assert Book.objects.all().count() == 2


def test__create_book_view__post_normal_user(db, user, client, create_book, delete_files_by_patern, text_file):
    book = create_book
    client.force_login(user)
    url = reverse('new_book')
    book_data = {
        'title': 'new',
        'author': book.author.pk,
        'description': 'Описание',
        'text': text_file,
        'genres': book.genres.all()[0].pk,
        'year_published': 1950,
    }

    response = client.post(url, book_data)

    assert response.status_code == 302
