FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk upgrade \
    && apk add --no-cache gcc musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir -U poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN /bin/sh -c set -ex; \
    poetry export --without dev --without-hashes -f requirements.txt -o requirements.txt
RUN pip install -U -r requirements.txt

COPY static ./static
COPY books_library ./books_library
COPY books ./books
COPY manage.py ./

RUN python manage.py collectstatic --noinput

CMD ["manage.py", "runserver", "0.0.0.0:8000"]