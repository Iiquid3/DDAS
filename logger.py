# Handles logging to both the terminal and a log file.

import logging

def setup_logger(log_to_file=True):
    """Set up a logger that logs to both terminal and a file."""
    logger = logging.getLogger('DuplicationRemover')
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('removal_log.txt')

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Set formatter for handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    if log_to_file:
        logger.addHandler(file_handler)

    return logger



