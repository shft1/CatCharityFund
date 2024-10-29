from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud


async def check_project_defore_edit(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get(
        obj_id=project_id,
        session=session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта не существует!'
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
):
    project = await charity_project_crud.get_project_by_name(
        name=name,
        session=session
    )
    if project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_full_amount(
        invested_amount: int,
        new_full_amount: int
):
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail=('Нелья установить значение '
                    'full_amount меньше уже вложенной суммы.')
        )