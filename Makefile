.PHONY: install migrations migrate run test

install:
       poetry install --no-root

migrations:
       poetry run python manage.py makemigrations

migrate:
       poetry run python manage.py migrate

run:
       poetry run python manage.py runserver

test:
       poetry run pytest
