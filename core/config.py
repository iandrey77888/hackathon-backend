import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret_test_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))

TEST_LOGIN = os.getenv("LOGIN", "admin")
TEST_PASSWORD = os.getenv("PASSWORD", "admin")

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, os.getenv("LOG_FILE", "app.log"))

DB_URL = os.getenv("DB_URL", "postgresql+psycopg2://mh_admin:2}0q0D6\\{zLfPB#@genshinlohs.ru:5432/ecmkontorskii")
MINIO_URL = os.getenv("MINIO_URL", "genshinlohs.ru:9000")
MINIO_ACCESS= os.getenv("MINIO_ACCESS", "kontorskii")
MINIO_SECRET = os.getenv("MINIO_SECRET", "your minio access key")
OCR_URL = os.getenv("OCR_URL", "your ocr endpoint")

'''
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
'''
LOG_LEVEL = os.getenv("LOG_LEVEL", 10)

TOKEN_URL = os.getenv("TOKEN_URL", "users/token")

#URL до API для обработки документов нейронкой
OCR_API_URL = os.getenv("OCR_API_URL", None)