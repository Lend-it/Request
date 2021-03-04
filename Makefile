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