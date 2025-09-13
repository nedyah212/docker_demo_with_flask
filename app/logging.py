import logging
import os
from datetime import datetime

# Custom formatter
formatter_console = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s: %(message)s')
formatter_file = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d: %(message)s')

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter_console)

# Create logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)  # Set minimum logging level
logger.addHandler(console_handler)

# Create 'logs' directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Create a dated log filename
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}_app.log"
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter_file)

# Add file handler to logger
logger.addHandler(file_handler)
