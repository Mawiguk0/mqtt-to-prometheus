# MQTT to Prometheus Exporter for Smart Garden

A lightweight exporter that reads sensor data from an MQTT broker and exposes it as Prometheus metrics. Designed for seamless integration with Grafana Stack Components like Loki/Promtail for monitoring and logging. Part of my upcoming Smart Garden project to automate and monitor garden systems using IoT devices.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9
- MQTT Broker (e.g., Mosquitto)
- Prometheus
- Grafana
- Promtail for log scraping (optional)

## Installation
You can use the docker images or build it yourself, choose for your comfort.

### Using Dockerhub
**_Coming soon!_**
### Build your own Images

1. **Clone the repository**:
   ```sh
   git clone https://github.com/Mawiguk0/mqtt-to-prometheus.git
   cd mqtt-to-prometheus
   ```

2. **Build and run the Docker containers**:
   ```sh
   docker-compose up --build
   ```

## Configuration

The project uses environment variables for configuration:

- `MQTT_BROKER`: Address of the MQTT broker.
- `MQTT_PORT`: Port of the MQTT broker (default: 1883).
- `MQTT_TOPIC`: MQTT topic to subscribe to.
- `PROMETHEUS_PORT`: Port for the Prometheus metrics server (default: 8000).
- `RETRY_INTERVAL`: Interval between retry attempts to connect to the MQTT broker (default: 5 seconds).

## Usage

1. **Start the service**:
   ```sh
   docker-compose up --build
   ```

2. **Access Prometheus metrics**:
   Open your browser and navigate to `http://localhost:8000/metrics`.

3. **View logs in Grafana**:
   Configure Grafana to read logs from Loki and explore the logs using the "Explore" feature.

## Health Check

The project includes a health check script to verify the service's health. The Docker container is configured to run this script periodically.

## Logging

Logs are structured using JSON format and are compatible with Grafana Loki for easy log aggregation and querying. The `promtail` service is used to scrape logs from Docker containers and send them to Loki.

## Prometheus Metrics

The following metrics are exposed:

- `mqtt_humidity`: Humidity from MQTT topic
- `mqtt_temperature`: Temperature from MQTT topic
- `mqtt_adc`: ADC value from MQTT topic
- `mqtt_battery`: Battery level from MQTT topic
- `mqtt_rssi`: RSSI from MQTT topic
- `mqtt_snr`: SNR from MQTT topic
- `mqtt_pferror`: Packet Frequency Error from MQTT topic
- `mqtt_packet_size`: Packet Size from MQTT topic
- `mqtt_last_data_received_timestamp`: Timestamp of the last data received

## Docker Compose Setup

The `docker-compose.yml` file sets up the following services:

- `mqtt_to_prometheus`: The main service that reads MQTT data and exposes Prometheus metrics.
- `prometheus`: The Prometheus service for scraping and storing metrics.
- `promtail`: The Promtail service for log scraping.

## Troubleshooting

- **MQTT Connection Issues**: Ensure the MQTT broker address and port are correctly configured.
- **Metrics Not Updating**: Check the MQTT topic for correct data and ensure the Prometheus scrape interval is appropriate.
- **Log Issues**: Verify that Promtail is correctly configured to scrape Docker logs.

## Architecture and Decision Records
For detailed information about the architecture and decision-making process behind this project, please refer to the following documents:

[Architecture Documentation](docs/architecture.md)  
[Architecture Decision Records](docs/decision/)
## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.