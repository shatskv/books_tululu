include .env
export

style: 
	ruff .
types:
	mypy .

tests_app:
	pytest .

check:
	make style types tests_app

run:
	python3 manage.py runserver