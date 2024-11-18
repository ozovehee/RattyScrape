import logging
from datetime import datetime

# Dictionary to store loggers by their component names
_loggers = {}
_logging_file = None

def get_logger(component):
    """
    Retrieve a logger for a given component. Ensures that the same logger
    is returned for the same component name.

    Args:
        component (str or object): The component or its name.
        logging_file (str, optional): File to which logs will be written.

    Returns:
        logging.Logger: A logger instance for the specified component.
    """
    global _logging_file
    # Determine the logger name
    if isinstance(component, str):
        logger_name = component
    else:
        logger_name = component.__class__.__name__

    # Return existing logger if one is already registered
    if logger_name in _loggers:
        return _loggers[logger_name]

    # Create a new logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # If logging_file is not provided, generate a default log file name
    if not _logging_file:
        current_time = datetime.now()
        time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        _logging_file = f"scraper_logs_{time_string}.log"

    # Create a file handler
    file_handler = logging.FileHandler(_logging_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter(f'%(asctime)s - {logger_name} - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Store the logger in the registry
    _loggers[logger_name] = logger

    # Log that the logger has been created
    logger.debug(f"<--- Logger started for {logger_name}")
    return logger

def set_logging_file(logging_file):
    """
    Changes the default, module wide logging file
    Args:
        logging_file (str): a file to log to by default
    """
    global _logging_file
    _logging_file = logging_file
    for  logger_name, logger in _loggers.items():
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
                handler.close()
        # Add a new file handler
        new_file_handler = logging.FileHandler(_logging_file)
        new_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - {logger_name} - %(levelname)s - %(message)s')
        new_file_handler.setFormatter(formatter)
        logger.addHandler(new_file_handler)

def reset_logger_registry():
    """
    Clear all registered loggers. Useful for testing or resetting the system.
    """
    _loggers.clear()
    global _logging_file
    _logging_file = None
