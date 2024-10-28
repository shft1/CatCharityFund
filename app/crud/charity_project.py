from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.schemas import CharityProjectUpdate

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_active_project(
        session: AsyncSession
    ):
        active_charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False
            )
        )
        return active_charity_project.scalars().all()

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
