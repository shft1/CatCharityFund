from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User

from .base import CRUDBase


class CRUDDonation(CRUDBase):
    @staticmethod
    async def get_user_donations(
        user: User,
        session: AsyncSession
    ):
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()
