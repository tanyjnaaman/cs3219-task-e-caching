from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file
from pathlib import Path

# assertions to check .env file
assert os.environ.get("ENV") in [
    "DEV",
    "PROD",
    "TEST",
], "ENV must be DEV, PROD, or TEST"
assert os.environ.get("MONGODB_CLOUD_URI") or os.environ.get("MONGODB_LOCAL_URI")
assert os.environ.get("PORT") is not None
assert os.environ.get("HOST") is not None
assert os.environ.get("FRONTEND_HOST") is not None
assert os.environ.get("JWT_SECRET") is not None

# enviroment
ENV_IS_PROD = os.environ.get("ENV") == "PROD"
ENV_IS_DEV = os.environ.get("ENV") == "DEV"
ENV_IS_TEST = os.environ.get("ENV") == "TEST"

# port
PORT = int(os.environ.get("PORT"))
HOST = os.environ.get("HOST")

# jwt
JWT_SECRET = os.environ.get("JWT_SECRET") or ""

# mongodb
MONGODB_CLOUD_URI = os.environ.get("MONGODB_CLOUD_URI")
MONGODB_LOCAL_URI = os.environ.get("MONGODB_LOCAL_URI")
MONGODB_URI = MONGODB_CLOUD_URI if ENV_IS_PROD else MONGODB_LOCAL_URI
MONGODB_DATABASE_NAME = "caching"

# mongodb tables
MONGODB_JSON_PATH = str(Path("./src/dev-data.json").resolve())
LINK_TABLE_NAME = "link"
MONGODB_TABLES = [LINK_TABLE_NAME]

# ======================== frontend ========================
FRONTEND_HOST = os.environ.get("FRONTEND_HOST") or ""
