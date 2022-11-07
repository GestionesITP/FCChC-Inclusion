#/bin/bash!
docker context use default
docker-compose --file docker-compose.test.yml up --build
docker tag inclusion-service_inclusion-api-test cchcdev.azurecr.io/inclusion-service:latest
docker push cchcdev.azurecr.io/inclusion-service:latest
docker context use azuretest1
docker compose --file docker-compose.azure.yml up --build