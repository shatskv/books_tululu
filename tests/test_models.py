from datetime import datetime
def test__Book_model__successfully(create_book, datetime_now):
    book = create_book(title='133', 
              description='34343', 
              text='343434',
              cover='dfdffdf',
              rating=4.5,
              year_published=1989,
              created_at=datetime_now,
              updated_at=datetime_now)
    assert book.title == '133'