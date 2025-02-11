.PHONY: install migrate run test

install:
       poetry install --no-root

migrations:
       poetry run python manage.py makemigrations

migrate:
       poetry run python manage.py migrate

run:
       poetry run python manage.py runserver 0.0.0.0:8000

test:
       poetry run pytest
