
from datetime import datetime, timezone
import uuid
from sqlalchemy import UUID, Column, DateTime
from config import Base


class ModelBase(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(tz=timezone.utc))

    def to_dict(self):
        """Returns a dictionary object of the instance"""
        dataset = {}

        for column in self.__table__.columns:
            key = column.name
            value = getattr(self, key)
            dataset.update({key: value})
        return dataset
