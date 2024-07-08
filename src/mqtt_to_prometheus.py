import os
import json
import time
import logging
from pythonjsonlogger import jsonlogger
import paho.mqtt.client as mqtt
from prometheus_client import start_http_server, Gauge

# Configuration from environment variables
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'home/OMG_ESP32_LORA/LORAtoMQTT')
PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 8000))
RETRY_INTERVAL = int(os.getenv('RETRY_INTERVAL', 5))  # retry interval in seconds

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Output the running configuration to log
logger.info("Configuration", extra={"MQTT_Broker": MQTT_BROKER, "MQTT_Port": MQTT_PORT, "MQTT_Topic": MQTT_TOPIC, "Prometheus_Port": PROMETHEUS_PORT})

# Prometheus gauges for different metrics
humidity_gauge = Gauge('mqtt_humidity', 'Humidity from MQTT topic', ['node_id'])
temperature_gauge = Gauge('mqtt_temperature', 'Temperature from MQTT topic', ['node_id'])
adc_gauge = Gauge('mqtt_adc', 'ADC value from MQTT topic', ['node_id'])
battery_gauge = Gauge('mqtt_battery', 'Battery level from MQTT topic', ['node_id'])
rssi_gauge = Gauge('mqtt_rssi', 'RSSI from MQTT topic', ['node_id'])
snr_gauge = Gauge('mqtt_snr', 'SNR from MQTT topic', ['node_id'])
pferror_gauge = Gauge('mqtt_pferror', 'Packet Frequency Error from MQTT topic', ['node_id'])
packet_size_gauge = Gauge('mqtt_packet_size', 'Packet Size from MQTT topic', ['node_id'])
last_data_received = Gauge('mqtt_last_data_received_timestamp', 'Timestamp of the last data received', ['node_id'])

# Callback when a message is received
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)

        node_id = data.get('node_id', 'unknown')

        if all(key in data for key in ('humidity', 'temperature', 'adc', 'battery', 'rssi', 'snr', 'pferror', 'packetSize')):
            humidity_gauge.labels(node_id=node_id).set(data.get('humidity', 0))
            temperature_gauge.labels(node_id=node_id).set(data.get('temperature', 0))
            adc_gauge.labels(node_id=node_id).set(data.get('adc', 0))
            battery_gauge.labels(node_id=node_id).set(data.get('battery', 0))
            rssi_gauge.labels(node_id=node_id).set(data.get('rssi', 0))
            snr_gauge.labels(node_id=node_id).set(data.get('snr', 0))
            pferror_gauge.labels(node_id=node_id).set(data.get('pferror', 0))
            packet_size_gauge.labels(node_id=node_id).set(data.get('packetSize', 0))
            # Update the last data received timestamp
            last_data_received.labels(node_id=node_id).set_to_current_time()
            logger.info("Updated metrics", extra={"node_id": node_id})
        else:
            logger.debug("Received incomplete data", extra={"node_id": node_id, "payload": payload})
    except json.JSONDecodeError:
        logger.error("Received non-JSON message", extra={"payload": message.payload.decode()})
    except Exception as e:
        logger.error("Error processing message", extra={"exception": str(e)})

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error("Failed to connect to MQTT broker", extra={"return_code": rc})

# Callback when the client disconnects from the broker
def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT broker")
    if rc != 0:
        logger.error("Unexpected disconnection", extra={"return_code": rc})

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Retry logic for connecting to MQTT broker
connected = False
while not connected:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        connected = True
    except Exception as e:
        logger.error("Failed to connect to MQTT broker", extra={"exception": str(e)})
        logger.info("Retrying", extra={"retry_interval": RETRY_INTERVAL})
        time.sleep(RETRY_INTERVAL)

# Start the Prometheus HTTP server
start_http_server(PROMETHEUS_PORT)

# Start the MQTT loop
client.loop_start()

logger.info("Service started", extra={"MQTT_Broker": MQTT_BROKER, "MQTT_Port": MQTT_PORT, "MQTT_Topic": MQTT_TOPIC, "Prometheus_Port": PROMETHEUS_PORT})

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Script interrupted, stopping...")
finally:
    client.loop_stop()
    client.disconnect()
    logger.info("Service stopped")