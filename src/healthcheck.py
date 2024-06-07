import requests
import logging
from pythonjsonlogger import jsonlogger
import os

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 8123))

def check_health():
    try:
        response = requests.get(f'http://localhost:{PROMETHEUS_PORT}/metrics')
        if response.status_code == 200:
            logger.info('Service is healthy')
            return 0
        else:
            logger.warning('Service is not healthy', extra={'status_code': response.status_code})
            return 1
    except Exception as e:
        logger.error('Health check failed', extra={'exception': str(e)})
        return 1

if __name__ == "__main__":
    exit(check_health())