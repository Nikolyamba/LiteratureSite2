import os
from loguru import logger


def setup_logging():

    logger.remove()  

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "..", "logs_api")
    os.makedirs(LOG_DIR, exist_ok=True)

    app_logs_path = os.path.join(LOG_DIR, "app.log")
    errors_logs_path = os.path.join(LOG_DIR, "error.log")

    logger.add(
        app_logs_path,
        level='INFO',
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        enqueue=True,
        colorize=True,
    format="<green>{time}</green> | | <level>{message}</level>",
    )
    

    logger.add(
        errors_logs_path,
        level='ERROR',
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        enqueue=True,
        colorize=True,
    format="<red>{time}</red> | | <level>{message}</level>",
    )

