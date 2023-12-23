from django.shortcuts import render
from books.models import Book, Author, Genre
from more_itertools import chunked
from math import ceil
from django.core.paginator import Paginator
from django.db.models import Count

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
    # print(page.number)
    # print(page.count())
    # page.count()
    # for num, books_per_page in enumerate(books_per_pages, start=1):
    #     books_chunked = list(chunked(books_per_page, 2))
    #     filepath = os.path.join(folder, filename_template.format(num))
    #     rendered_page = template.render(books=books_chunked, 
    #                                     num_pages=len(books_per_pages),
    #                                     current_page=num)
    
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


def authors_view(request):
    authors = authors = Author.objects.annotate(num_books=Count('books')).order_by('-num_books')
    block_name = 'Авторы'

    return render(request, 'authors.html', {'authors': authors, 'block_name': block_name})

def books_by_author_view(request, author_id):
    author = Author.objects.get(pk=author_id)
    books = author.books.all()
    block_name = f'Книги автора {author.fullname}'
    chunked_books = list(chunked(books, BOOKS_PER_ROW))
    paginator = Paginator(chunked_books, ceil(BOOKS_PER_PAGE/BOOKS_PER_ROW))
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request, 'paginator.html', {'page': page, 'block_name': block_name})


