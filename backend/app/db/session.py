import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


# รองรับ: CON-TECH-01

def get_database_url() -> str:
    return os.getenv("DATABASE_URL", "sqlite:///:memory:")


def build_engine():
    database_url = get_database_url()
    engine_kwargs = {}

    if database_url.startswith("sqlite"):
        engine_kwargs.update(
            {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        )

    return create_engine(database_url, **engine_kwargs)


engine = build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
