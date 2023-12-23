import argparse
import logging
import os
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

logger = logging.getLogger('tululu')

def check_response(response):
    response.raise_for_status()
    check_for_redirect(response)


def download_txt(url, filename, folder='books'):
    response = requests.get(url)
    check_response(response)
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    Path(folder).mkdir(parents=True, exist_ok=True)
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def check_for_redirect(response):
    if response.status_code == 302:
        raise requests.HTTPError(f'code: 404, No book for this url')


def parse_args_from_terminal():
    parser = argparse.ArgumentParser(
    description='Задайте диапазон скачивания книг:'
                )
    parser.add_argument('-s', '--book_start_id', help="Начальный ID книги", type=int, default=1)
    parser.add_argument('-e', '--book_end_id', help="Конечный ID книги", type=int, default=10)
    args = parser.parse_args()
    book_start_id = args.book_start_id
    book_end_id = args.book_end_id
    return book_start_id, book_end_id


def parse_book_page(book_html):
    page_soup = BeautifulSoup(book_html, 'lxml')
    selector = '#content h1'
    name_and_author = page_soup.select_one(selector).text

    selector = "a[href^='/txt.php']"
    book_href = page_soup.select_one(selector)
    
    selector = ".bookimage img[src]"
    image_route = page_soup.select_one(selector).get('src')

    selector = "span.d_book a[href]"
    genres_hrefs = page_soup.select(selector)
    genres = [genre_href.text for genre_href in genres_hrefs]

    selector = ".texts .black"
    comment_classes = page_soup.select(selector)
    comments = [comment_class.text for comment_class in comment_classes]

    book_route = book_href.get('href') if book_href else None
    
    name, author = name_and_author.split('::')
    author = author.strip()
    name = name.strip()
    return {'name': name,
            'author': author, 
            'book_route': book_route,
            'image_route': image_route, 
            'comments': comments,
            'genres': genres}


def fetch_books(book_start_id=1, book_end_id=10):
    url_book_template = 'https://tululu.org/b{}/'
    book_filename_template ='{}. {}.txt'
    books_folder='books/'
    images_folder='images/'
    image_filename_template='{}.jpg'
    book_id_in_local_lib = 1

    for book_id in range(book_start_id, book_end_id + 1):
        url = url_book_template.format(book_id)
       
        try:
            response = requests.get(url, allow_redirects=False)
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
            continue

        book_link = urljoin(url, book_parsed['book_route'])
        image_link = urljoin(url, book_parsed['image_route'])

        book_filename = book_filename_template.format(book_id_in_local_lib, book_parsed['name'])
        image_filename = image_filename_template.format(book_id_in_local_lib)

        try:
            download_txt(book_link, book_filename, books_folder)
            download_image(image_link, image_filename, images_folder)
        except requests.ConnectionError as e:
            logger.error(f'Connection error while download book files: {e}')
            time.sleep(5)
        except requests.HTTPError as e:
            logger.error(f'HTTP error while download book files: {e}')
        else:
            book_id_in_local_lib += 1


def main():
    book_start_id, book_end_id = parse_args_from_terminal()
    fetch_books(book_start_id=book_start_id, book_end_id=book_end_id)


if __name__ == '__main__':
    main()
