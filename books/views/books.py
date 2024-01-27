from math import ceil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from more_itertools import chunked

from books.models import Author, Book, Genre


@login_required
def books_view(request):
    books = Book.objects.all()

    chunked_books = list(chunked(books, settings.BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(settings.BOOKS_PER_PAGE/settings.BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    block_name = 'Все книги'
    
    return render(request, 'books/books.html', {'page': page, 'block_name': block_name})


@login_required
def book_view(request: HttpRequest, book_id: int):
    book = Book.objects.get(pk=book_id)
    block_name = f'Книга {book.title}'
    return render(request, 'books/book_page.html', {'book': book, 'block_name': block_name})


def home_view(request: HttpRequest):
    return redirect('genres/')


def authors_view(request: HttpRequest):
    authors = Author.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Авторы'

    return render(request, 'authors.html', {'authors': authors, 'block_name': block_name})


def genres_view(request: HttpRequest):
    genre = Genre.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Жанры'

    return render(request, 'genres.html', {'genres': genre, 'block_name': block_name})

@login_required
def books_by_author_view(request: HttpRequest, author_id: int):
    author = Author.objects.get(pk=author_id)
    books = author.books.all()

    block_name = f'Книги автора "{author.fullname}"'
    chunked_books = list(chunked(books, settings.BOOKS_PER_ROW))

    paginator = Paginator(chunked_books, ceil(settings.BOOKS_PER_PAGE/settings.BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'books/books.html', {'page': page, 'block_name': block_name})


@login_required
def books_by_genre_view(request: HttpRequest, genre_id: int):
    genre = Genre.objects.get(pk=genre_id)
    books = genre.books.all()
    block_name = f'Жанр "{genre.name}"'
    chunked_books = list(chunked(books, settings.BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(settings.BOOKS_PER_PAGE/settings.BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'books/books.html', {'page': page, 'block_name': block_name})
