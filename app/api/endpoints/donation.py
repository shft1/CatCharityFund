from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import current_superuser, current_user, get_async_session
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationDBSuperuser

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
    pass


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
