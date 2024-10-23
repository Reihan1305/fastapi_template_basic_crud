from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from basic_template.db.dependencies import get_db_session
from basic_template.db.models.dummy_model import DummyModel


class DummyDAO:
    """Class for accessing the dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def create_dummy_model(self, name: str) -> None:
        """
        Add a single dummy to the session.

        :param name: Name of the dummy.
        """
        self.session.add(DummyModel(name=name))

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: Limit of dummies.
        :param offset: Offset of dummies.
        :return: List of dummies.
        """
        raw_dummies = await self.session.execute(
            select(DummyModel).limit(limit).offset(offset),
        )
        return list(raw_dummies.scalars().fetchall())

    async def filter(self, name: Optional[str] = None) -> List[DummyModel]:
        """
        Get specific dummy models.

        :param name: Name of the dummy instance.
        :return: List of dummy models.
        """
        query = select(DummyModel)
        if name:
            query = query.where(DummyModel.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def get_by_id(self, id: int) -> Optional[DummyModel]:
        """
        Get a dummy model by its ID.

        :param id: ID of the dummy.
        :return: The dummy model or None if not found.
        """
        query = select(DummyModel).where(DummyModel.id == id)
        rows = await self.session.execute(query)
        result = rows.scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="Dummy not found")
        return result

    async def delete_dummies(self, id: int) -> None:
        """
        Delete a dummy model by its ID.

        :param id: ID of the dummy to delete.
        """
        dummy_to_delete = await self.session.get(DummyModel, id)
        if dummy_to_delete:
            await self.session.delete(dummy_to_delete)
            await self.session.commit()

    async def update_dummies(self, id: int, name: str) -> DummyModel:
        """
        Update a dummy model's name.

        :param id: ID of the dummy to update.
        :param name: New name for the dummy.
        :return: Updated dummy model.
        """
        dummy_to_update = await self.session.get(DummyModel, id)
        if not dummy_to_update:
            raise HTTPException(status_code=404, detail="Dummy not found")

        dummy_to_update.name = name
        await self.session.commit()

        return dummy_to_update
