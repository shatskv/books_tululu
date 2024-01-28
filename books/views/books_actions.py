from math import ceil

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from more_itertools import chunked

from books.forms import BookForm, SearchForm
from books.models import Book, BookProgress


@login_required
def search_view(request: HttpRequest):
    if request.method == 'POST':
        search_value = request.POST.get('search_field', '').strip()
        request.session['search_value'] = search_value
    
    search_value = request.session.get('search_value')
    if not search_value:
        return redirect('/books')
    books = Book.objects.filter(Q(title__icontains=search_value) | Q(author__fullname__icontains=search_value))
    chunked_books = list(chunked(books, settings.BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(settings.BOOKS_PER_PAGE/settings.BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    if not books:
        block_name = 'По вашему запросу ничего не найдено'
    else:
        block_name = 'Книги по вашему запросу'
    return render(request, 'books/books.html', {'page': page, 'block_name': block_name})


@login_required
def search_details_view(request):
    block_name = 'Детальный поиск'
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            request.session['search_form'] = request.POST
            return redirect('search_result')
    else:
        form = SearchForm()
    return render(request, 'books/search_details.html', {'block_name': block_name, 'form': form})


@login_required
def search_details_result_view(request: HttpRequest):
    form = SearchForm(request.session.get('search_form'))
    if not request.session.get('search_form') or not form.is_valid():
        return redirect('search_details')
    
    cd = form.cleaned_data
    title = cd.get('title')
    author = cd.get('author')
    genre = cd.get('genre')
    rating_from = cd.get('rating_from')
    rating_to = cd.get('rating_to')
    description = cd.get('description')

    books = Book.objects.all()

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__fullname__icontains=author)
    if genre:
        books = books.filter(genre__name__icontains=genre)
    if description:
        books = books.filter(description__icontains=description)
    if rating_from:
        books = books.filter(rating__gte=rating_from)
    if rating_to:
        books = books.filter(rating__lte=rating_to)

    chunked_books = list(chunked(books, settings.BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(settings.BOOKS_PER_PAGE/settings.BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if not books:
        block_name = 'По вашему запросу ничего не найдено'
    else:
        block_name = 'Книги по вашему запросу'
    return render(request, 'books/books.html', {'page': page, 'block_name': block_name})
    

@staff_member_required
def create_book_view(request: HttpRequest):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('books', book_id=book.pk)
    else:
        form = BookForm()
    block_name = 'Создание книги'
    return render(request, 'books/new_book.html', {'form': form, 'block_name': block_name})


@login_required
def reader_book_view(request: HttpRequest, book_id: int):
    book = Book.objects.get(pk=book_id)
    if book.text:
        with open(book.text.path, 'r') as file:
            text = file.read()
    else:
        text = ''
    lines = text.splitlines(keepends=True)
    chunks = ["".join(lines[i:i + settings.ROWS_TEXT_PER_PAGE]) for i in range(0, len(lines), settings.ROWS_TEXT_PER_PAGE)]
    paginator = Paginator(chunks, 1)
    page_number = request.GET.get('page')
   
    if text:
        book_progress = BookProgress.objects.get_or_create(
            book=book,
            user=request.user
        )[0]
        page_number = book_progress.page if book_progress.page is not None \
                      and page_number is None else page_number
        book_progress.page = page_number
        book_progress.page = 1 if not page_number and paginator.num_pages == 1 else  book_progress.page
        book_progress.num_pages = paginator.num_pages
        book_progress.save()
    page_number = 1 if page_number is None else page_number
    page = paginator.get_page(page_number)
    block_name = f'Книга "{book.title}"'
    return render(request, 'reader.html', {'block_name': block_name, 'page': page})


@staff_member_required
def update_book_view(request: HttpRequest, book_id: int):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('books', book_id=book.pk)
    else:
        form = BookForm(instance=book)
    block_name = f'Изменение книги "{book.title}"'
    return render(request, 'books/update_book.html', {'form': form, 'book': book, 'block_name': block_name})
