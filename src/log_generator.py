import uuid
import time
import random
import logging
import os
from datetime import datetime
from pythonjsonlogger import jsonlogger

# Setup logging directory
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logger = logging.getLogger()
log_file = os.path.join(log_dir, 'system.log')
logHandler = logging.FileHandler(log_file)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s %(service)s %(id)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Sample log messages
ERROR_MESSAGES = [
    "Connection refused to database",
    "API rate limit exceeded",
    "Memory allocation failed",
    "Disk space critical",
    "Authentication failed multiple times",
    "Unexpected service shutdown",
    "Network timeout occurred",
]

SERVICES = ["database", "api", "auth", "storage", "network"]

def generate_log():
    while True:
        # Randomly choose severity and message
        level = random.choice([logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL])
        message = random.choice(ERROR_MESSAGES)
        service = random.choice(SERVICES)
        
        # Log the message
        logger.log(level, message, extra={'service': service, 'id': str(uuid.uuid4())})
        
        # Random delay between 1 to 5 seconds
        time.sleep(random.uniform(1, 5))

if __name__ == "__main__":
    print("Starting log generation...")
    generate_log()