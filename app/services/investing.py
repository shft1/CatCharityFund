from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

# ЛЮТЫЙ ТРЕЕЕЕЕШ надо тестить и рефакторить


class Investing:
    donation_free_money = []  # [[donation, money], [donation, money]]

    @classmethod
    async def charity_project_investing(
        cls,
        charity_project: CharityProject,
        session: AsyncSession
    ):
        for donation, free_money in cls.donation_free_money:
            if (charity_project.invested_amount + free_money <
                    charity_project.full_amount):
                donation.invested_amount += free_money
                donation.fully_invested = True
                donation.close_date = datetime.now()
                charity_project.invested_amount += free_money
            elif (charity_project.invested_amount + free_money ==
                    charity_project.full_amount):
                donation.invested_amount += free_money
                donation.fully_invested = True
                donation.close_date = datetime.now()
                charity_project.invested_amount += free_money
                charity_project.fully_invested = True
                charity_project.close_date = datetime.now()
                break
            elif (charity_project.invested_amount + free_money >
                    charity_project.full_amount):
                free_money = ((charity_project.invested_amount + free_money) - charity_project.full_amount)
                donation.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
                charity_project.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
                charity_project.fully_invested = True
                charity_project.close_date = datetime.now()
                break
        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)
        return charity_project

    @classmethod
    async def donation_investing(
        cls,
        donation: Donation,
        active_charity_projects: list[CharityProject],
        session: AsyncSession
    ):
        free_money = donation.full_amount
        for charity_project in active_charity_projects:
            if (charity_project.invested_amount + free_money <
                    charity_project.full_amount):
                donation.invested_amount += free_money
                donation.fully_invested = True
                donation.close_date = datetime.now()
                charity_project.invested_amount += free_money
                break
            elif (charity_project.invested_amount + free_money ==
                    charity_project.full_amount):
                donation.invested_amount += free_money
                donation.fully_invested = True
                donation.close_date = datetime.now()
                charity_project.invested_amount += free_money
                charity_project.fully_invested = True
                charity_project.close_date = datetime.now()
                break
            elif (charity_project.invested_amount + free_money >
                    charity_project.full_amount):
                free_money = (charity_project.invested_amount + free_money) - charity_project.full_amount
                donation.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
                charity_project.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
                charity_project.fully_invested = True
                charity_project.close_date = datetime.now()
                cls.donation_free_money.append([donation, free_money])
        session.add_all(active_charity_projects)
        session.add(donation)
        await session.commit()
        await session.refresh(donation)
        return donation
