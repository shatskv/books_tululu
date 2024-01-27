from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from books.forms import UserRegistrationForm
from books.models import BookProgress


@login_required
def user_profile_view(request: HttpRequest):
    block_name = 'Профиль'
    books_progress = request.user.reading_books.all().order_by('book')
    return render(request, 'user/profile.html', {'block_name': block_name, 'books_progress': books_progress})


@login_required
def delete_book_progress(request: HttpRequest, progress_id):
    book_progress = BookProgress.objects.get(pk=progress_id)
    book_progress.delete()
    return redirect('profile')


def register_user_view(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    block_name = 'Регистрация пользователя'
    return render(request, 'user/registration.html', {'form': form, 'block_name': block_name})
