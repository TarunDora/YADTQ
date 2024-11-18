#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" &>/dev/null
}

# Start Kafka
echo "Starting Kafka service..."
if command_exists systemctl; then
    sudo systemctl start kafka
    echo "Kafka service started."
else
    echo "Systemd not available. Please start Kafka manually."
fi

# Start Redis
echo "Starting Redis service..."
if command_exists systemctl; then
    sudo systemctl start redis
    echo "Redis service started."
else
    echo "Systemd not available. Please start Redis manually."
fi

# Create Kafka topic 'TaskQueue' with 3 partitions
echo "Creating Kafka topic 'TaskQueue' with 3 partitions..."
if command_exists kafka-topics.sh; then
    kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic TaskQueue
    echo "Kafka topic 'TaskQueue' created successfully."
else
    echo "'kafka-topics.sh' not found. Please ensure Kafka is installed and the bin directory is in your PATH."
    exit 1
fi

echo "Setup complete!"
