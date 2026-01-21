import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename = "backend/logs/logs.log",
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    )
