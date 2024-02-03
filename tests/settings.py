import logging

from books_library.settings import *

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',

}
logging.getLogger('faker').setLevel(logging.ERROR)