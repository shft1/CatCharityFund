from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_wrapper
from app.core.user import current_superuser
from app.schemas import CharityProjectDB
from app.services.managers import charity_project_manager, spreadsheets_create

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
    projects = await charity_project_manager.get_pjs_sorted_by_closing_speed(
        session=session
    )
    spreadsheet_id = await spreadsheets_create(wrapper)
    return projects