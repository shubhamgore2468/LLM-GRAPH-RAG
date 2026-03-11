import logging
import sys

def setup_logging():
    """
    Configures the root logger for the application.
    This setup directs logs to the console with a consistent format.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Configure the logger
    logging.basicConfig(
        level=logging.INFO,  # Set the minimum level of logs to capture
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout  # Direct logs to standard output (the console)
    )