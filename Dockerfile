# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=home/OMG_ESP32_LORA/LORAtoMQTT
ENV PROMETHEUS_PORT=8000
ENV RETRY_INTERVAL=5

# Run mqtt_to_prometheus.py when the container launches
CMD ["python", "./src/mqtt_to_prometheus.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD ["python", "./src/healthcheck.py"]
