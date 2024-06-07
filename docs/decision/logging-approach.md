# ADR 002: Logging Approach

## Title

Implement Structured Logging with Integration to Loki

## Status

Accepted

## Context

Effective logging is critical for monitoring, debugging, and maintaining the MQTT to Prometheus Exporter. The project requires a logging solution that provides structured logs, integrates with existing monitoring tools, and supports centralized log management.

## Decision

We decided to use structured logging with JSON format and integrate with Grafana Loki for centralized log management. The logging approach includes the following components and practices:

1. **Structured Logging**:
   - Use JSON format for logs to ensure they are structured and easily parseable.
   - Utilize the `python-json-logger` library for implementing structured logging in Python.

2. **Log Levels**:
   - Use appropriate log levels (DEBUG, INFO, WARNING, ERROR) to categorize log messages.
   - Set default log level to INFO, with the option to increase verbosity to DEBUG for development and troubleshooting.

3. **Integration with Loki**:
   - Use Promtail to scrape logs from Docker containers and forward them to Loki.
   - Configure Promtail with a `promtail-config.yml` file to ensure proper log collection and labeling.

4. **Centralized Log Management**:
   - Store and manage logs in Grafana Loki, providing a centralized location for querying and analyzing logs.
   - Integrate with Grafana for visualizing logs and creating alerts based on log data.

## Consequences

1. **Improved Log Management**:
   - Centralized log storage in Loki simplifies log management and provides a single source of truth for logs.
   - Structured logs in JSON format enhance the ability to search, filter, and analyze log data.

2. **Enhanced Observability**:
   - Integration with Grafana allows for advanced visualization and correlation of logs with metrics, improving overall observability.
   - Developers can quickly identify and troubleshoot issues using comprehensive log data.

3. **Complexity**:
   - Introducing Loki and Promtail adds complexity to the deployment and configuration.
   - Requires proper setup and management of Promtail agents and Loki instances.

4. **Resource Usage**:
   - Additional resources are needed to run Promtail and Loki services, which may impact system performance.
   - Structured logging may increase the size of log files compared to plain text logs.

## Alternatives Considered

1. **Plain Text Logging**:
   - Pros: Simpler setup, lower resource usage.
   - Cons: Less structured, harder to parse and analyze.

2. **Using Elasticsearch for Logging**:
   - Pros: Powerful search capabilities, widely used.
   - Cons: More resource-intensive, higher complexity in setup and management.

3. **Using Fluentd for Log Forwarding**:
   - Pros: Flexible and extensible log forwarding.
   - Cons: Additional component to manage, overlap with Promtail capabilities.

## Conclusion

Adopting structured logging with JSON format and integrating with Loki provides a scalable, efficient, and powerful logging solution for the MQTT to Prometheus Exporter. This approach enhances log management and observability, ensuring the project can be effectively monitored and maintained.
