from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractBaseModel(Base):
    __abstract__ = True
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_data = Column(DateTime)
    close_date = Column(DateTime)
