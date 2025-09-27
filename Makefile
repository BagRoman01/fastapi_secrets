.PHONY: build push build-push

COMPOSE = docker compose -f docker-compose.yaml

build:
	@echo "Building images..."
	$(COMPOSE) build

up:
	@echo "Docker compose up..."
	$(COMPOSE) up

push:
	@echo "Pushing images..."
	$(COMPOSE) push

build-push: build push

build-up: build up