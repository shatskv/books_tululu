"""
URL configuration for books_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from books.views.books import (authors_view, book_view, books_by_author_view,
                               books_by_genre_view, books_view, genres_view,
                               home_view)
from books.views.books_actions import (create_book_view, reader_book_view,
                                       search_details_result_view,
                                       search_details_view, search_view,
                                       update_book_view)
from books.views.user import (delete_book_progress_view, logout_view,
                              register_user_view, user_profile_view)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('accounts/register/', register_user_view, name='register'),
    path('accounts/profile/', user_profile_view, name='profile'),
    path('books/', books_view, name='all_books'),
    path('books/progress/<int:progress_id>', delete_book_progress_view, name='delete_progress'),
    path('', home_view),
    path('books/<int:book_id>', book_view, name='books'),
    path('authors/', authors_view),
    path('genres/', genres_view),
    path('authors/<int:author_id>', books_by_author_view, name='authors'),
    path('genres/<int:genre_id>', books_by_genre_view, name='genres'),
    path('search/', search_view, name='search'),
    path('search_details/', search_details_view, name='search_details'),
    path('search_details/result/', search_details_result_view, name='search_result'),
    path('books/new_book/', create_book_view, name='new_book'),
    path('books/<int:book_id>/update', update_book_view, name='update_book'),
    path('books/<int:book_id>/reader/', reader_book_view, name='reader'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
