import pytest

from books.forms import BookForm, SearchForm, UserRegistrationForm


@pytest.mark.parametrize(
    ('title', 'author', 'description', 'text', 'cover', 'genres', 'year_published', 'is_valid'),
    [
    ('Название', 'author_obj', 'desc', 'text_file', 'image_file', 'list_genre_obj_pk', None, True),
    ('Название', 'author_obj', 'desc', 'text_file', 'image_file', None, None, False),
    ('Название', None, 'desc', 'text_file', 'image_file', None, 'year_published', False),
    (None, None, 'desc', 'text_file', 'image_file', None, 'year_published', False),
    ('Название', 'author_obj', 'desc', 'text_file', None, 'list_genre_obj_pk', 'year', True),
    ('Название', 'author_obj', 'desc', None, 'image_file', 'list_genre_obj_pk', 'year', True),
    ('Название', 'author_obj', 'desc', None, 'image_file', 'list_genre_obj_pk', 'year33', False)
    ]
)
def test__BookForm__validity(db, get_fixture_value, title, author, description, text, cover, genres, year_published, is_valid, delete_files_by_patern):
    author = get_fixture_value(author)
    text = get_fixture_value(text)
    cover = get_fixture_value(cover)
    year_published = get_fixture_value(year_published)
    genres = get_fixture_value(genres)

    form_data = {
        'title': title,
        'author': author().pk if author else None,
        'text': text,
        'description': description,
        'cover': cover,
        'genres': genres() if genres else None,
        'year_published': year_published
    }

    form = BookForm(data=form_data)
    
    assert form.is_valid() is is_valid

    if callable(text):
        delete_files_by_patern(text, form.text.path)
    
    if callable(cover):
        delete_files_by_patern(cover, form.cover.path)


@pytest.mark.parametrize(
    ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_valid'),
    [
    ('user1', None, None, None, '1235dfdffd', '1235dfdffd', True),
    (None, None, None, None, '1235dfdffd', '1235dfdffd', False),
    ('user1', None, None, None, '1235dfdffd', '1235d33fdffd', False),
    ('user1', 'dddff', 'dsdfds', 'tt@mail.ru', '1235dfdffd', '1235dfdffd', True),
    ('user1', 'dddff', 'dsdfds', 'ttddmail.ru', '1235dfdffd', '1235dfdffd', False),
])
def test__UserRegistrationForm__validity(db, username, first_name, last_name, email, password1, password2, is_valid, get_fixture_value):
    form_data = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password1': password1,
        'password2': password2
    }
    form = UserRegistrationForm(data=form_data)

    assert form.is_valid() is is_valid, form.errors


@pytest.mark.parametrize(
    ('title', 'author', 'description', 'genre', 'rating_to', 'rating_from', 'is_valid'),
    [
    ('ddf', 'dfdf', 'dfdfdf', 'dfdfdf', 0.5, 10, True),
    (None, None, None, None, None, None, True),
    (None, None, None, None, None, None, True),
    (None, None, None, None, '5', None, True),
    (None, None, None, None, None, '9', True),
    (None, None, None, None, None, -5, False),
    (None, None, None, None, 12, None, False),
    (None, None, None, None, 4, 12, False),
   


])
def test__SearchForm__validity(title, author, description, genre, rating_to, rating_from, is_valid):
    form_data = {
        'title': title,
        'author': author,
        'description': description,
        'genre': genre,
        'rating_to': rating_to,
        'rating_from': rating_from,
        'is_valid': is_valid
    }
    form = SearchForm(data=form_data)

    assert form.is_valid() is is_valid
