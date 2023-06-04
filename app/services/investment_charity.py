from datetime import datetime

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def get_first_obj(cl, session: AsyncSessionLocal):
    first_obj = await session.execute(
        select(cl).where(cl.fully_invested == False).order_by(cl.create_date)  # noqa
    )

    return first_obj.scalars().first()


async def investment_charity(db_obj, session: AsyncSessionLocal):
    # Найти первый проект по дате
    first_charity_project = await get_first_obj(CharityProject, session)

    # Найти первый донат по дате
    first_donation = await get_first_obj(Donation, session)

    if first_donation is None or first_charity_project is None:
        await session.refresh(db_obj)
        return db_obj

    # Доступная сумма пожертвования
    available_donation = first_donation.full_amount - first_donation.invested_amount

    # Сколько нужно пожертвования
    how_much_donation = first_charity_project.full_amount - first_charity_project.invested_amount

    def donation_collected():
        first_donation.fully_invested = True
        first_donation.close_date = datetime.now()

    def charity_project_collected():
        first_charity_project.fully_invested = True
        first_charity_project.close_date = datetime.now()

    if available_donation < how_much_donation:
        donation_collected()

    if available_donation == how_much_donation:
        charity_project_collected()
        donation_collected()

    if available_donation > how_much_donation:
        charity_project_collected()

    first_charity_project.invested_amount += available_donation
    first_donation.invested_amount += available_donation

    session.add(first_donation)
    session.add(first_charity_project)

    await session.commit()
    await session.refresh(first_donation)
    await session.refresh(first_charity_project)

    return await investment_charity(db_obj, session)
