import json
import logging
import os
import time
from argparse import ArgumentParser
from itertools import count
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand

from books.utils.tululu import (check_for_redirect, check_response,
                                download_image, download_txt, parse_book_page)

logger = logging.getLogger(__name__)
JSON_PATH = 'books.json'

def parse_terminal_args(options: dict[str, Any]) -> dict[str, Any]:
    return  {'start_page': options.get('start_page'),
             'end_page': options.get('end_page'),
             'skip_imgs': options.get('skip_imgs'),
             'skip_txt': options.get('skip_txt')
            }


class Command(BaseCommand):
    help = 'Скачивает книги с сайта\n'

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--start_page', help="Начальная страница", type=int, default=1)
        parser.add_argument('--end_page', help="Конечная страница", type=int, default=10)
        parser.add_argument('--skip_imgs', help="Не загружать обложки книг", action='store_true')
        parser.add_argument('--skip_txt', help="Не загружать тексты книг", action='store_true')

    def handle(self, *args: list, **options: dict[Any, Any]) -> None:
        terminal_args = parse_terminal_args(options)
        fetch_fantastic_books(**terminal_args)


def get_book_urls_from_page(main_page_url: str, page_html: str) -> list[str]:
    page_soup = BeautifulSoup(page_html, 'lxml')
    selector = ".bookimage a"
    book_blocks = page_soup.select(selector)
    book_urls = [urljoin(main_page_url, block.get('href')) for block in book_blocks] # type: ignore[type-var]
    return book_urls # type: ignore[return-value]


def fetch_fantastic_books(start_page: int=1, end_page: int | None=None, dest_folder: 
                          str=settings.BOOKS_DIR, # type: ignore[misc]
                          json_path: str=JSON_PATH, skip_imgs: bool=False, skip_txt: bool=False) -> None:
    url_template = 'https://tululu.org/l55/{}'

    books_folder = 'books'
    images_folder = 'images'
    image_filename_template = '{}.jpg'
    book_filename_template = '{}.txt'
    books_folder = os.path.join(dest_folder, books_folder)
    images_folder = os.path.join(dest_folder, images_folder)
    book_urls = []
    for num_page in count(start_page):
        if num_page == end_page:
            break
        try:
            url = url_template.format(num_page)
            response = requests.get(url, allow_redirects=False)
            response.raise_for_status()
        except requests.ConnectionError as e:
            logger.error(f'url: {url} Connection error: {e}')
            time.sleep(5)
            continue
        except requests.HTTPError as e:
            logger.error(f'url: {url} HTTP error: {e}')
            continue

        try:
            check_for_redirect(response)
        except requests.HTTPError as e:
            logger.error(e)
            break

        page_book_urls = get_book_urls_from_page(url, response.text)
        book_urls += page_book_urls

    books = []
    for book_url in book_urls:
        try:
            response = requests.get(book_url, allow_redirects=False)
            check_response(response)
        except requests.ConnectionError as e:
            logger.error(f'url: {url} Connection error: {e}')
            time.sleep(5)
            continue
        except requests.HTTPError as e:
            logger.error(f'url: {url} HTTP error: {e}')
            continue

        page_html = response.text
        book_parsed = parse_book_page(page_html)

        if not book_parsed.get('book_route'):
            logger.error(f'No book text for this url: {book_url}')
            continue
        _, book_id = book_url.split('/b')
        book_id = book_id.strip('/')

        book_link = urljoin(book_url, book_parsed['book_route'])
        image_link = urljoin(book_url, book_parsed['image_route'])

        book_filename = book_filename_template.format(book_parsed['name'])
        image_filename = image_filename_template.format(book_id)
        try:
            book_path = download_txt(book_link, book_filename, books_folder) if not skip_txt else None
            img_path = download_image(image_link, image_filename, images_folder) if not skip_imgs else None
        except requests.ConnectionError as e:
            logger.error(f'Connection error while download book files: {e}')
            time.sleep(5)
            continue
        except requests.HTTPError as e:
            logger.error(f'HTTP error while download book files: {e}')
            continue
        except requests.ReadTimeout as e:
            logger.error(f'Read timeout error : {e}')
            continue
        book = {
            'title': book_parsed['name'],
            'author': book_parsed['author'],
            'img_src': img_path,
            'book_path': book_path,
            'description': book_parsed['description'],
            'comments': book_parsed['comments'],
            'genres': book_parsed['genres']
        }
        books.append(book)

    if json_path.count(os.sep) == 0:
        json_path = os.path.join(dest_folder, json_path)
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(books, file, indent=4, ensure_ascii=False)
