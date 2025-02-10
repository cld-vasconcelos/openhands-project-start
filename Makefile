.PHONY: install migrate migrations run test

install:
       poetry install --no-root

migrate:
       poetry run python manage.py migrate

migrations:
       poetry run python manage.py makemigrations

run:
       poetry run python manage.py runserver

test:
       poetry run pytest
