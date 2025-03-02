from sqlalchemy import create_engine, schema
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    Session,
)
from config.env_configs import configs
from sqlalchemy.ext.declarative import declarative_base
from typing import Iterator

environment = configs.ENV

engine = (
    create_engine(configs.TEST_DB_URL)
    if environment == "test"
    else create_engine(
        configs.DB_URL,
        connect_args={"options": "-c timezone=utc"},
        pool_size=20,
        max_overflow=0,
        pool_timeout=300,
        pool_recycle=300,
        pool_pre_ping=True,
        pool_use_lifo=True,
        isolation_level="READ COMMITTED",
    )
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = (
    declarative_base()
    if environment == "test"
    else declarative_base(metadata=schema.MetaData(schema="public"))
)

Base.query = scoped_session(SessionLocal).query_property()


def get_db() -> Iterator[Session]:
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
