from django.urls import reverse
from books.models import BookProgress, User

def test__delete_book_progress_view__delete(db, book_progress, client):
    book_progress
    before_delete = BookProgress.objects.all().count()

    client.force_login(book_progress.user)

    url = reverse('delete_progress', kwargs={'progress_id': book_progress.pk})

    response = client.get(url)

    assert response.status_code == 302
    assert before_delete == 1
    assert BookProgress.objects.all().count() == 0


def test__user_profile_view__redirect(db, client):
    url = reverse('profile')

    response = client.get(url)

    assert response.status_code == 302 


def test__user_profile_view__profile(db, client, user):
    client.force_login(user)
    url = reverse('profile')

    response = client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert user.username in content


def test__logout_view__suceessfully(db, user, client):
    client.force_login(user)

    url = reverse('logout')
    response = client.post(url, follow=True)

    content = response.content.decode()

    assert response.status_code == 200
    assert 'Спасибо, что зашли на наш сайт!' in content


def test__register_user_view__get(db, client):
    url = reverse('register')

    response = client.get(url)

    assert response.status_code == 200


def test__register_user_view__get(db, client):
    url = reverse('register')

    user_data = {
        'username': 'ddfddfd',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'ddf@mail.ru',
        'password1': 'dsfdfsdfSFF33434',
        'password2': 'dsfdfsdfSFF33434'
    }

    response = client.post(url, user_data, follow=True)

    assert response.status_code == 200
    assert User.objects.all().count() == 1
