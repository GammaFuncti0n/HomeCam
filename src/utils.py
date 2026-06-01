import logging
import os

def setup_loggers(log_path='/log') -> None:
    '''
    user logger
    '''
    os.makedirs(log_path, exist_ok=True)
    user_logger = logging.getLogger("user_requests")
    user_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(log_path, "user_requests.log"), encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s | user_id=%(user_id)s | username=%(username)s | %(message)s"))

    user_logger.addHandler(file_handler)
    user_logger.propagate = False
    '''
    system logger
    '''
    system_logger = logging.getLogger("system")
    system_logger.setLevel(logging.INFO)

    system_file_handler = logging.FileHandler(os.path.join(log_path, "system.log"), encoding="utf-8")
    system_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

    system_logger.addHandler(system_file_handler)
    system_logger.propagate = False