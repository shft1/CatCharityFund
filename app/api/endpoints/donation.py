from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationDBSuperuser
from app.services.investing import donation_investing

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    pass


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    projects = await charity_project_crud.get_multi(
        session=session
    )
    investing_donation = await donation_investing(
        new_donation, projects, session
    )
    return investing_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    pass
