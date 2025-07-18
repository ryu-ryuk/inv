.DEFAULT_GOAL := help
.PHONY: help up down import-data test

help:
	@echo "Available commands:"
	@echo "  make up           - Build images and start all services."
	@echo "  make down         - Stop all services and remove database volume."
	@echo "  make import-data  - Run the data import script."
	@echo "  make test         - Run the unit tests and coverage report."

# Starts the entire setup
up:
	@echo "Building images and starting services..."
	@docker compose up --build -d

# Stops the entire setup and cleans up the database volume
down:
	@echo "Stopping services and removing volumes..."
	@docker compose down -v

# Runs the data import script
import-data:
	@echo "Importing stock data from CSV..."
	@docker compose exec api python import_data.py

# Runs the unit tests
test:
	@echo "Running tests and generating coverage report..."
	@docker compose exec api coverage run -m unittest discover tests && docker compose exec api coverage report -m
