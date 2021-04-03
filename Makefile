SHELL := /bin/bash # Use bash syntax
CURRENT_DIR := $(shell pwd)

build:
	chmod +x entrypoint.sh
	sudo docker-compose -f docker-compose.dev.yml build

run:
	sudo docker-compose -f docker-compose.dev.yml up

run-silent:
	sudo docker-compose -f docker-compose.dev.yml up -d

run-build:
	sudo docker-compose -f docker-compose.dev.yml up --build

test:
	sudo docker-compose -f docker-compose.dev.yml run request python manage.py test

lint:
	sudo docker-compose -f docker-compose.dev.yml run request black .

check-db:
	sudo docker-compose -f docker-compose.dev.yml exec db psql -U postgres

down:
	sudo docker-compose -f docker-compose.dev.yml down

recreate-db:
	sudo docker-compose -f docker-compose.dev.yml run request python manage.py recreate-db

cov-html:
	sudo docker-compose -f docker-compose.dev.yml run request python manage.py cov;
	google-chrome  $(CURRENT_DIR)/htmlcov/index.html;