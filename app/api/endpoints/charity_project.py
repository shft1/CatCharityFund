from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_defore_edit,
                                check_project_full_amount,
                                check_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.investing import project_investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_project = await charity_project_crud.create(
        obj=charity_project,
        session=session
    )
    donations = await donation_crud.get_multi(
        session=session
    )
    investing_project = await project_investing(
        project=new_project,
        donations=donations,
        session=session
    )
    return investing_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_defore_edit(
        project_id=project_id,
        session=session
    )
    if charity_project_in.name is not None:
        await check_project_name_duplicate(
            name=charity_project_in.name,
            session=session
        )
    if charity_project_in.full_amount is not None:
        await check_project_full_amount(
            invested_amount=project.invested_amount,
            new_full_amount=charity_project_in.full_amount
        )
    update_project = await charity_project_crud.update(
        obj_model=project,
        obj_in=charity_project_in,
        session=session
    )
    return update_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    pass
