.PHONY: help build up down restart logs shell db-shell test clean

help:
@echo "Nazigi Stamford Bus SMS Service - Docker Commands"
@echo "=================================================="
@echo "make build      - Build Docker images"
@echo "make up         - Start containers"
@echo "make down       - Stop containers"
@echo "make restart    - Restart containers"
@echo "make logs       - View logs"
@echo "make shell      - Access Flask container shell"
@echo "make db-shell   - Access PostgreSQL shell"
@echo "make test       - Run tests"
@echo "make clean      - Clean up Docker resources"

build:
docker compose build

up:
docker compose up -d

down:
docker compose down

restart:
docker compose restart

logs:
docker compose logs -f

shell:
docker compose exec web bash

db-shell:
docker compose exec db psql -U nazigi_user -d nazigi_sms

test:
docker compose exec web python -m pytest

clean:
docker compose down -v
docker system prune -f
