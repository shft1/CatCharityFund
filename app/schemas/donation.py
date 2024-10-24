from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuperuser(DonationDBUser):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[str]

    class Config:
        orm_mode = True
