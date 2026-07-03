from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

TEST_DATABASE_URL = settings.database_url

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)