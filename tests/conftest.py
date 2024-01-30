import pytest
from datetime import datetime
from books.models import Book, Genre, Author, BookProgress



@pytest.fixture
def datetime_now():
    return datetime.now()

@pytest.fixture
def create_book():
    def inner(title=None, 
              description=None, 
              text=None,
              cover=None,
              rating=None,
              year_published=None,
              created_at=None,
              updated_at=None
            ):
        book = Book(title=title, 
                    description=description, 
                    text=text,
                    cover=cover,
                    rating=rating,
                    year_published=year_published,
                    created_at=created_at,
                    updated_at=updated_at)
        return book
    return inner