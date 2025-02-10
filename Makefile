.PHONY: install migrate makemigrations run test

install:
       poetry install

migrate:
       poetry run python user_auth_system/manage.py migrate

makemigrations:
       poetry run python user_auth_system/manage.py makemigrations

run:
       poetry run python user_auth_system/manage.py runserver

test:
       poetry run python user_auth_system/manage.py test
