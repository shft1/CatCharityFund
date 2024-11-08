from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.integrations import get_wrapper
from app.schemas import CharityProjectDB
from app.services.managers import (charity_project_manager,
                                   set_user_permissions, spreadsheets_create,
                                   spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=list[CharityProjectDB],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper: Aiogoogle = Depends(get_wrapper)
):
    projects = await charity_project_manager.get_projects_by_completion_rate(
        session=session
    )
    spreadsheet_id = await spreadsheets_create(wrapper)
    await set_user_permissions(wrapper, spreadsheet_id)
    await spreadsheets_update_value(wrapper, projects, spreadsheet_id)
    return projects
