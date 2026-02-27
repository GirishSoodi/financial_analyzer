import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "financial_ai")

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"
)

# Retry logic (VERY IMPORTANT for Docker)
MAX_RETRIES = 15
RETRY_DELAY = 3

for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(
            DATABASE_URL,
            pool_size=20,
            max_overflow=40,
            pool_pre_ping=True
        )

        # Test connection
        with engine.connect() as conn:
            print("✅ Connected to MySQL")

        break

    except OperationalError:
        print(f"⏳ MySQL not ready... retrying ({attempt+1}/{MAX_RETRIES})")
        time.sleep(RETRY_DELAY)

else:
    raise Exception("❌ Could not connect to MySQL after retries")

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()