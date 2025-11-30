.PHONY: build up down push build-push build-up

COMPOSE = docker compose -f docker-compose.yaml
IMAGE_NAME = secrets-app:latest

build:
	@echo "Building image..."
	docker build -t $(IMAGE_NAME) .

up:
	@echo "Docker compose up..."
	$(COMPOSE) up -d

down:
	@echo "Docker compose down..."
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f secrets

push:
	@echo "Pushing image..."
	docker push $(IMAGE_NAME)

build-push: build push

build-up: build up
