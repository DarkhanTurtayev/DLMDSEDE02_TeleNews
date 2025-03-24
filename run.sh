#!/bin/bash

echo "Starting TeleNews Pipeline"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed!"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed!"
    exit 1
fi

if docker compose ps | grep -q 'running'; then
    echo "Containers are already running."
    read -p "Do you want to restart them? (y/n): " choice
    if [[ "$choice" == [Yy] ]]; then
        echo "Restarting containers!"
        docker compose down
    else
        echo "Ok, well, bye then!"
        exit 0
    fi
fi

docker compose build
docker compose up -d 

echo "TeleNews running, please visit http://localhost:3000 to see dashboards"

# Auto-open (partially working)
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:3000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:3000
elif [[ "$OSTYPE" == "msys"* ]]; then
    start http://localhost:3000
fi