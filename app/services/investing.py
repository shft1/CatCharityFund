from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

# ЛЮТЫЙ ТРЕЕЕЕЕШ надо тестить и рефакторить


# есть идея свободные деньги у пожертвования вычислять по разнице между
# суммой пожертвования и суммой, которая ушла на инвестиции


async def donation_investing(
        donation: Donation,
        active_project: list[CharityProject],
        session: AsyncSession
):
    free_money = donation.full_amount
    for project in active_project:
        if project.invested_amount + free_money < project.full_amount:
            project.invested_amount += free_money
            donation.invested_amount += free_money
            donation.fully_invested = True
            donation.close_date = datetime.now()
            break
        elif project.invested_amount + free_money == project.full_amount:
            project.invested_amount += free_money
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += free_money
            donation.fully_invested = True
            donation.close_date = datetime.now()
            break
        elif project.invested_amount + free_money > project.full_amount:
            free_money = ((project.invested_amount + free_money) -
                          project.full_amount)
            investing_amount = project.full_amount - project.invested_amount
            project.invested_amount += investing_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += investing_amount
    session.add_all(active_project)
    session.add(donation)
    await session.commit()
    await session.refresh(donation)
    return donation


async def project_investing(
        project: CharityProject,
        donations: list[Donation],
        session: AsyncSession
):
    for donation in donations:
        if donation.fully_invested:
            continue
        free_money = donation.full_amount - donation.invested_amount
        if project.invested_amount + free_money < project.full_amount:
            project.invested_amount += free_money
            donation.invested_amount += free_money
            donation.fully_invested = True
            donation.close_date = datetime.now()
        elif project.invested_amount + free_money == project.full_amount:
            project.invested_amount += free_money
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += free_money
            donation.fully_invested = True
            donation.close_date = datetime.now()
            break
        elif project.invested_amount + free_money > project.full_amount:
            investing_amount = project.full_amount - project.invested_amount
            project.invested_amount += investing_amount
            project.fully_invested = True
            project.close_date = datetime.now()
            donation.invested_amount += investing_amount
            break
    session.add_all(donations)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project




# class Investing:
#     donation_free_money = []  # [[donation, money], [donation, money]]

#     @classmethod
#     async def charity_project_investing(
#         cls,
#         charity_project: CharityProject,
#         session: AsyncSession
#     ):
#         for donation, free_money in cls.donation_free_money:
#             if (charity_project.invested_amount + free_money <
#                     charity_project.full_amount):
#                 donation.invested_amount += free_money
#                 donation.fully_invested = True
#                 donation.close_date = datetime.now()
#                 charity_project.invested_amount += free_money
#             elif (charity_project.invested_amount + free_money ==
#                     charity_project.full_amount):
#                 donation.invested_amount += free_money
#                 donation.fully_invested = True
#                 donation.close_date = datetime.now()
#                 charity_project.invested_amount += free_money
#                 charity_project.fully_invested = True
#                 charity_project.close_date = datetime.now()
#                 break
#             elif (charity_project.invested_amount + free_money >
#                     charity_project.full_amount):
#                 free_money = ((charity_project.invested_amount + free_money) - charity_project.full_amount)
#                 donation.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
#                 charity_project.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
#                 charity_project.fully_invested = True
#                 charity_project.close_date = datetime.now()
#                 break
#         new_donations = [donation for donation, _ in cls.donation_free_money]
#         session.add_all(new_donations)
#         session.add(charity_project)
#         await session.commit()
#         await session.refresh(charity_project)
#         return charity_project

#     @classmethod
#     async def donation_investing(
#         cls,
#         donation: Donation,
#         active_charity_projects: list[CharityProject],
#         session: AsyncSession
#     ):
#         free_money = donation.full_amount
#         if active_charity_projects:
#             for charity_project in active_charity_projects:
#                 if (charity_project.invested_amount + free_money <
#                         charity_project.full_amount):
#                     donation.invested_amount += free_money
#                     donation.fully_invested = True
#                     donation.close_date = datetime.now()
#                     charity_project.invested_amount += free_money
#                     break
#                 elif (charity_project.invested_amount + free_money ==
#                         charity_project.full_amount):
#                     donation.invested_amount += free_money
#                     donation.fully_invested = True
#                     donation.close_date = datetime.now()
#                     charity_project.invested_amount += free_money
#                     charity_project.fully_invested = True
#                     charity_project.close_date = datetime.now()
#                     break
#                 elif (charity_project.invested_amount + free_money >
#                         charity_project.full_amount):
#                     free_money = (charity_project.invested_amount + free_money) - charity_project.full_amount
#                     donation.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
#                     charity_project.invested_amount += (charity_project.full_amount - charity_project.invested_amount)
#                     charity_project.fully_invested = True
#                     charity_project.close_date = datetime.now()
#                     cls.donation_free_money.append([donation, free_money])
#         else:
#             cls.donation_free_money.append([donation, free_money])
#         session.add_all(active_charity_projects)
#         session.add(donation)
#         await session.commit()
#         await session.refresh(donation)
#         return donation
