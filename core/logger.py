import logging
import os
from logging.handlers import TimedRotatingFileHandler
import core.config as cfg


os.makedirs(cfg.LOG_DIR, exist_ok=True)

logger = logging.getLogger("app_logger")
logger.setLevel(cfg.LOG_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setLevel(cfg.LOG_LEVEL)

file_handler = TimedRotatingFileHandler(
    cfg.LOG_FILE,
    when="D",          # ротация по дням (можно "H" - по часам, "M" - по минутам)
    interval=1,        # каждые 1 день
    backupCount=7,     # хранить 7 файлов
    encoding="utf-8"
)

file_handler = logging.FileHandler(cfg.LOG_FILE, encoding="utf-8")
file_handler.setLevel(cfg.LOG_LEVEL)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
