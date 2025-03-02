from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.models.base import Base
from uuid import UUID

T = TypeVar("T", bound=Base)  # type: ignore


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def save(self, obj_in: T) -> T:
        """Create a new record in the database."""
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def get(self, obj_id: UUID) -> Optional[T]:
        """Retrieve a single record by its ID."""
        result = await self.session.get(self.model, obj_id)
        return result

    async def get_all(self) -> List[T]:
        """Retrieve all records from the table."""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def update(self, obj_id: UUID, update_data: dict) -> Optional[T]:
        """Update a record by its ID."""
        obj = await self.get(obj_id)
        if not obj:
            return None
        for key, value in update_data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: UUID) -> bool:
        """Delete a record by its ID."""
        obj = await self.get(obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
