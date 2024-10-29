from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas import CharityProjectUpdate
from app.services.close_object import close_object

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get(
        obj_id: int,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.id == obj_id)
        )
        return db_obj.scalars().first()

    @staticmethod
    async def get_project_by_name(
        name: str,
        session: AsyncSession
    ):
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return db_obj.scalars().first()

    @staticmethod
    async def update(
        obj_model: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ):
        obj_model_dict = jsonable_encoder(obj_model)
        obj_in_dict = obj_in.dict(exclude_unset=True)
        for field in obj_model_dict:
            if field in obj_in_dict:
                setattr(obj_model, field, obj_in_dict[field])
        if obj_model.invested_amount == obj_model.full_amount:
            close_object(obj_model)
        session.add(obj_model)
        await session.commit()
        await session.refresh(obj_model)
        return obj_model

    @staticmethod
    async def delete(
        obj_model: CharityProject,
        session: AsyncSession
    ):
        await session.delete(obj_model)
        await session.commit()
        return obj_model


charity_project_crud = CRUDCharityProject(CharityProject)
