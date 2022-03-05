#!/bin/bash
# Build and publish weather_checking app.
docker build -t weather-app weather_checking
#docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY  -e API_KEY=$API_KEY -d -p 80:80 --name weather-app weather-app
docker tag weather-app dwoodbridge/weather-app
docker push dwoodbridge/weather-app

# Build and publish cron app.
docker build -t cron-app cron
#docker run --name cron-app cron-app
docker tag cron-app dwoodbridge/cron-app
docker push dwoodbridge/cron-app

# run docker compose which creates a network between cron-app and weather-app
docker-compose --env-file .env up