AIRFLOW_VERSION=2.7.3

# build docker
build-docker:
	docker build -f docker/Dockerfile .

# Airflow
build-start:
	docker compose -f docker/docker-compose.yml up --build

start:
	docker compose -f docker/docker-compose.yml up

stop:
	docker compose -f docker/docker-compose.yml down


