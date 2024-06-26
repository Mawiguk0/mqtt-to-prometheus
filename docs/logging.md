### Logging

The MQTT to Prometheus Exporter project uses structured logging to provide clear and detailed log entries. This section describes the logging approach, log levels, and sample log entries to help understand and troubleshoot the system.

#### Logging Approach

- **Structured Logging**: The project uses structured logging with JSON format, making logs easily parseable and searchable.
- **Library**: The `python-json-logger` library is used to implement structured logging in Python.
- **Integration with Loki**: Logs are collected by Promtail and forwarded to Loki for centralized log management and querying.
- **Environment Variables**: Environment variables are used to configure the logging level and other settings.

#### Log Levels

The project uses the following log levels to categorize log messages:

- **DEBUG**: Detailed information for debugging purposes.
- **INFO**: General information about the application's normal operations.
- **WARNING**: Indications of potential issues or important events that are not errors.
- **ERROR**: Errors and exceptions that occur during the application's execution.

#### Sample Log Entries

Here are some sample log entries to illustrate the structure and content of the logs generated by the project:

**INFO Level Log**
```json
{
  "message": "Service started",
  "MQTT_Broker": "10.101.0.4",
  "MQTT_Port": 1883,
  "MQTT_Topic": "home/OMG_ESP32_LORA/LORAtoMQTT",
  "Prometheus_Port": 8000,
  "level": "INFO",
  "timestamp": "2024-06-07T08:40:35.333Z"
}
```

**DEBUG Level Log**
```json
{
  "message": "Received incomplete data",
  "node_id": "unknown",
  "payload": "{\"frequency\":868000000,\"txpower\":14,\"spreadingfactor\":7,\"signalbandwidth\":125000,\"codingrate\":5,\"preamblelength\":8,\"syncword\":\"0x12\",\"enablecrc\":true,\"invertiq\":false,\"onlyknown\":false}",
  "level": "DEBUG",
  "timestamp": "2024-06-07T08:46:21.322Z"
}
```

**ERROR Level Log**
```json
{
  "message": "Error processing message",
  "exception": "ValueError: Invalid data format",
  "level": "ERROR",
  "timestamp": "2024-06-07T08:42:21.318Z"
}
```

#### Configuration

To configure the logging settings, use the following environment variables:

- **LOG_LEVEL**: Set the desired logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default is `INFO`.

Example configuration in `docker-compose.yml`:

```yaml
mqtt_to_prometheus:
  build: .
  environment:
    - MQTT_BROKER=mqtt_broker
    - MQTT_PORT=1883
    - MQTT_TOPIC=home/OMG_ESP32_LORA/LORAtoMQTT
    - PROMETHEUS_PORT=8000
    - RETRY_INTERVAL=5
    - LOG_LEVEL=INFO
  ports:
    - "8000:8000"
  restart: always
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
```

#### Viewing Logs in Grafana

Logs can be viewed and queried in Grafana by configuring Loki as a data source. Use the following steps to view logs:

1. **Add Loki as a Data Source**:
   - Navigate to Grafana settings and add a new data source.
   - Select "Loki" and configure the URL to point to your Loki instance.

2. **Explore Logs**:
   - Use the "Explore" feature in Grafana to query logs using the labels and fields in the structured log entries.
   - Filter logs by `level`, `message`, or other fields to find relevant information.

By following this approach, you can ensure that logs are structured, easily searchable, and provide valuable insights into the operation of the MQTT to Prometheus Exporter project.