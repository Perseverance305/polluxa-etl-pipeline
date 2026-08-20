import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "polluxa_dw")
POSTGRES_USER = os.getenv("POSTGRES_USER", "polluxa")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")