from config.db import engine, Base


def init_db():
    """Initialize database"""
    Base.metadata.create_all(engine)
