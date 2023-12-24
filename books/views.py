from math import ceil

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from more_itertools import chunked
from django.db.models.functions import Lower

from books.models import Author, Book, Genre

BOOKS_PER_PAGE = 20
BOOKS_PER_ROW = 2


# Create your views here.

def books_view(request):
    books = Book.objects.all()
    chunked_books = list(chunked(books, BOOKS_PER_ROW))

    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    block_name = 'Все книги'
    print(page.paginator.num_pages)
    
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def authors_view(request):
    authors = Author.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Авторы'

    return render(request, 'authors.html', {'authors': authors, 'block_name': block_name})


def genres_view(request):
    genre = Genre.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Жанры'

    return render(request, 'genres.html', {'genres': genre, 'block_name': block_name})


def books_by_author_view(request, author_id):

    author = Author.objects.get(pk=author_id)
    books = author.books.all()

    block_name = f'Книги автора {author.fullname}'
    chunked_books = list(chunked(books, BOOKS_PER_ROW))

    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def books_by_genre_view(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    books = genre.books.all()
    block_name = f'Жанр "{genre.name}"'
    chunked_books = list(chunked(books, BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def search_view(request):
    search_value = request.POST.get('search_field', '').strip()
    print(f'|{search_value}|')
    # books = Book.objects.filter(Q(title__icontains=search_value) | Q(author__fullname__icontains=search_value))
    books = Book.objects.filter(Q(title__icontains=search_value))
    # books = Book.objects.filter(title__lower__icontains=search_value.lower())
    # books = Book.objects.annotate(lower_title=Lower('title')).filter(lower_title__contains=search_value.lower())
    print(books)
    chunked_books = list(chunked(books, BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    print(list(page.object_list))
    if not books:
        block_name = 'По вашему запросу ничего не найдено'
        # template = 'books.html'
    else:
        block_name = 'Книги по вашему запросу'
        # template = 'paginator.html'
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})

def book_view(request, book_id):
    book = Book.objects.get(pk=book_id)
    block_name = f'Книга {book.title}'
    return render(request, 'book_page.html', {'book': book, 'block_name': block_name})

def search_details_view(request):
    pass

def create_book_view(request):
    pass

def update_book_view(request, book_id):
    pass
