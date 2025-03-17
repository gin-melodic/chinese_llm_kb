#!/bin/bash

# Check environment variables file
if [ ! -f .env ]; then
    echo "Error: .env file does not exist, please create and configure environment variables"
    exit 1
fi

# Ensure data directory exists
mkdir -p data/documents

# Start service with docker-compose
docker-compose up -d

echo "Service started"
echo "API address: http://localhost:$(grep API_PORT .env | cut -d '=' -f2)/docs"
echo "You can view logs with the following command:"
echo "docker-compose logs -f api"
