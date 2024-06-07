# Smart Garden MQTT to Prometheus Exporter Architecture

## Overview

The MQTT to Prometheus Exporter is a key component of the Smart Garden project. It reads sensor data from an MQTT broker and exposes it as Prometheus metrics. This allows for seamless monitoring and integration with Grafana for visualization and Loki for structured logging.

## Components

### 1. MQTT Broker

- **Role**: Acts as a central hub for collecting data from various IoT sensors deployed in the garden.
- **Example**: Mosquitto.

### 2. MQTT to Prometheus Exporter

- **Role**: Subscribes to topics on the MQTT broker, processes the incoming messages, and exposes them as Prometheus metrics.
- **Main Components**:
  - `mqtt_to_prometheus.py`: Main script for subscribing to MQTT topics and exporting metrics.
  - `healthcheck.py`: Script to verify the health of the exporter service.

### 3. Prometheus

- **Role**: Scrapes and stores metrics exposed by the exporter, making them available for querying and alerting.
- **Configuration**: Defined in `prometheus.yml`.

### 4. Grafana

- **Role**: Provides a powerful visualization layer for Prometheus metrics and Loki logs.
- **Dashboards**: Pre-configured dashboards for visualizing garden sensor data.

### 5. Loki

- **Role**: Centralized logging system that stores structured logs from various components.
- **Integration**: Promtail scrapes logs from Docker containers and sends them to Loki.

### 6. Promtail

- **Role**: Collects logs from Docker containers and forwards them to Loki.
- **Configuration**: Defined in `promtail-config.yml`.

## Data Flow

1. **Sensor Data Collection**:
   - IoT sensors in the garden collect data (e.g., humidity, temperature) and publish it to specific MQTT topics.

2. **MQTT Broker**:
   - The MQTT broker receives and stores messages from the sensors.

3. **MQTT to Prometheus Exporter**:
   - The exporter subscribes to relevant MQTT topics.
   - Processes incoming messages and extracts sensor data.
   - Exposes the data as Prometheus metrics.

4. **Prometheus Scraping**:
   - Prometheus periodically scrapes metrics from the exporter.
   - Stores the metrics in its time-series database.

5. **Grafana Visualization**:
   - Grafana queries Prometheus to retrieve metrics.
   - Displays the metrics in dashboards for monitoring.

6. **Logging with Loki**:
   - Promtail scrapes logs from Docker containers.
   - Sends the logs to Loki for centralized storage and querying.

## Directory Structure

```plaintext
mqtt-to-prometheus/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── promtail-config.yml
├── src/
│   ├── mqtt_to_prometheus.py
│   └── healthcheck.py
└── docs/
    └── architecture.md
```

## Configuration

### Environment Variables

- `MQTT_BROKER`: Address of the MQTT broker.
- `MQTT_PORT`: Port of the MQTT broker (default: 1883).
- `MQTT_TOPIC`: MQTT topic to subscribe to.
- `PROMETHEUS_PORT`: Port for the Prometheus metrics server (default: 8000).
- `RETRY_INTERVAL`: Interval between retry attempts to connect to the MQTT broker (default: 5 seconds).

### Docker Compose

The `docker-compose.yml` file sets up the services required for the project:
- `mqtt_to_prometheus`: Main service for exporting metrics.
- `prometheus`: Metrics storage and querying.
- `promtail`: Log scraping and forwarding to Loki.

## Logging

Logs are structured using JSON format and are compatible with Grafana Loki for easy log aggregation and querying. The `promtail` service is used to scrape logs from Docker containers and send them to Loki.

## Health Check

The health check script ensures the service is running correctly by verifying the Prometheus metrics endpoint. The Docker container is configured to run this script periodically.

## Conclusion

The MQTT to Prometheus Exporter is a crucial component for monitoring the Smart Garden. By integrating MQTT, Prometheus, Grafana, and Loki, it provides a comprehensive solution for collecting, storing, and visualizing sensor data, as well as centralized logging for easier debugging and analysis.
