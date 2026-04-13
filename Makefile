# Variables
APP_NAME=line-bot-gdrive
REGION=asia-east1
PORT=8080

.PHONY: help install run build clean deploy-cloud-run

help:
	@echo "Usage:"
	@echo "  make install            Install dependencies"
	@echo "  make get-token          Run the OAuth2 token generation script"
	@echo "  make run                Run the application locally"
	@echo "  make build              Build the Docker image"
	@echo "  make deploy-cloud-run   Deploy the application to Google Cloud Run"

install:
	pip install -r requirements.txt

get-token:
	python get_token.py

run:
	python -m src.main

build:
	docker build -t $(APP_NAME) .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

deploy-cloud-run:
	@echo "Starting deployment to Cloud Run..."
	@if [ -z "$(LINE_CHANNEL_SECRET)" ] || [ -z "$(LINE_CHANNEL_ACCESS_TOKEN)" ] || [ -z "$(GOOGLE_DRIVE_FOLDER_ID)" ] || [ -z "$(GOOGLE_SERVICE_ACCOUNT_JSON)" ]; then \
		echo "Error: One or more environment variables are missing (LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, GOOGLE_DRIVE_FOLDER_ID, GOOGLE_SERVICE_ACCOUNT_JSON)"; \
		exit 1; \
	fi
	gcloud run deploy $(APP_NAME) \
		--source . \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--set-env-vars "LINE_CHANNEL_SECRET=$(LINE_CHANNEL_SECRET),LINE_CHANNEL_ACCESS_TOKEN=$(LINE_CHANNEL_ACCESS_TOKEN),GOOGLE_DRIVE_FOLDER_ID=$(GOOGLE_DRIVE_FOLDER_ID),GOOGLE_SERVICE_ACCOUNT_JSON='$(GOOGLE_SERVICE_ACCOUNT_JSON)'"
