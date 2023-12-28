# Приложение на Django c библиотекой книг, скачанных с  [tululu.org](https://tululu.org/)

Приложение умеет: 
- Скачивать книги с указанного сайта
- Составлять библиотеку из этих книг

## Как установить

- Python3 должен быть установлен
- Затем используйте `pip` (или `pip3`, еслить есть конфликт с Python2) для установки зависимостей: 
    ```
    pip install -r requirements.txt
    ```

- Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.


## Как пользоваться
Сначала нужно запустить скрипт парсинга, затем само приложение

### Cкрипт парсинга c [tululu.org](https://tululu.org/) запускается через терминал:

```
   python3 manage.py get_books_from_tululu
```
- Файлы будут сохранены в папку **books_downloads**
- Можно указать следующие аргументы в терминале:
    - Начальная страница раздела
    - Конечная страница раздела
    - Выключение загрузки обложек
    - Выключение загрузки текстов книг
    ```
    $ python3 manage.py get_books_from_tululu -h
    usage: manage.py get_books_from_tululu [-h] [-s START_PAGE] [-e END_PAGE] [-si] [-st] [--version] [-v {0,1,2,3}] [--settings SETTINGS]
                                       [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color] [--skip-checks]

    Скачивает книги с сайта

    options:
    -h, --help            show this help message and exit
    -s START_PAGE, --start_page START_PAGE
                        Начальная страница
    -e END_PAGE, --end_page END_PAGE
                        Конечная страница
    -si, --skip_imgs      Не загружать обложки книг
    -st, --skip_txt       Не загружать тексты книг
    ```
- Подождать несколько минут пока скачаются книги, время зависит от количества указанных страниц

### Для запуска самого приложения нужно выполнить следующее:
- Указать подключение к базе данных
- Применять миграции, в их составе есть датамиграция для загрузки книг в базу:
    ```
    python3 manage.py migrate
    ``` 
- Запустить сервер:
    ```
     python3 manage.py runserver
    ```
- Скрипт и приложение Django записывают в логи ошибки при выполнении а папку **logs**
 

### Цель проекта

Код написан в образовательный целях на онлайн-курсе для python-разработчиков [learn.python.ru/advanced/](https://learn.python.ru/advanced/)
