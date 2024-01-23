from math import ceil

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from more_itertools import chunked

from .models import Author, Book, Genre
from .forms import BookForm, AuthorForm, GenreForm

BOOKS_PER_PAGE = 20
BOOKS_PER_ROW = 2
MIN_RATING = 0
MAX_RATING = 10


def convert_str_rating_to_float(text: str, is_max=True) -> float:
    default = MAX_RATING if is_max else MIN_RATING
    try:
        num = float(text)
    except:
        return default
    return min(num, default) if is_max else max(num, default)


# Create your views here.

def books_view(request):
    books = Book.objects.all()

    chunked_books = list(chunked(books, BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    block_name = 'Все книги'
    
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def authors_view(request):
    authors = Author.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Авторы'

    return render(request, 'authors.html', {'authors': authors, 'block_name': block_name})


def genres_view(request):
    genre = Genre.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Жанры'

    return render(request, 'genres.html', {'genres': genre, 'block_name': block_name})


def books_by_author_view(request, author_id: int):
    author = Author.objects.get(pk=author_id)
    books = author.books.all()

    block_name = f'Книги автора "{author.fullname}"'
    chunked_books = list(chunked(books, BOOKS_PER_ROW))

    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def books_by_genre_view(request, genre_id: int):
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
    books = Book.objects.filter(Q(title__icontains=search_value) | Q(author__fullname__icontains=search_value))
    chunked_books = list(chunked(books, BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    if not books:
        block_name = 'По вашему запросу ничего не найдено'
    else:
        block_name = 'Книги по вашему запросу'
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def book_view(request, book_id: int):
    book = Book.objects.get(pk=book_id)
    block_name = f'Книга {book.title}'
    return render(request, 'book_page.html', {'book': book, 'block_name': block_name})


def search_details_view(request):
    block_name = 'Детальный поиск'
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        genre = request.POST.get('genre', '').strip()
        rating_from = request.POST.get('rating_from', '').strip().replace(',', '.')
        rating_to = request.POST.get('rating_to', '').strip()
        description = request.POST.get('description', '').strip()
        

        books = Book.objects.all()
        filters = {}
        if title:
            filters['title__icontains'] = title
        if author:
            filters['author__fullname__icontains'] = author
        if genre:
            filters['genre__name__icontains'] = genre
        if description:
            filters['description__icontains'] = description

        if rating_from or rating_to:
                rating_from = convert_str_rating_to_float(rating_from, False)
                rating_to = convert_str_rating_to_float(rating_to)
                filters['rating__gte'] = rating_from
                filters['rating__lte'] = rating_to

        if filters:
            books = books.filter(**filters)

        chunked_books = list(chunked(books, BOOKS_PER_ROW))
        paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        if not books:
            block_name = 'По вашему запросу ничего не найдено'
        else:
            block_name = 'Книги по вашему запросу'
        return render(request, 'paginator.html', {'page': page, 'block_name': block_name})

    return render(request, 'search_details.html', {'block_name': block_name})


def create_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('books', book_id=book.pk)
    else:
        form = BookForm()
    block_name = 'Создание книги'
    return render(request, 'new_book.html', {'form': form, 'block_name': block_name})


def show_txt_file(request, book_id: int):
    book = Book.objects.get(pk=book_id)
    if book.text:
        with open(book.text.path, 'r') as file:
            text = file.read()
    else:
        text = ''
    block_name = f'Книга "{book.title}"'
    return render(request, 'reader.html', {'block_name': block_name, 'text': text})




def update_book_view(request, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books', book_id=book.pk)
    else:
        form = BookForm(instance=book)
    block_name = f'Изменение книги "{book.title}"'
    return render(request, 'update_book.html', {'form': form, 'book': book, 'block_name': block_name})
