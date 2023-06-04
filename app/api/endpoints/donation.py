from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationGetAllDB
from app.services.investment_charity import investment_charity

router = APIRouter()

session: AsyncSession = Depends(get_async_session)


@router.get('/',
            response_model=List[DonationGetAllDB],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],
            summary='Все пожертвования')
async def get_all_donation(session=session):
    """
    <h3>
        <font color="#6B7A99">Получение всех пожертвований.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Суперпользователь.</font></p>
    """

    return await donation_crud.get_multi(session)


@router.post('/',
             response_model=DonationDB,
             response_model_exclude_none=True,
             summary='Создание пожертвования')
async def create_new_charity_project(donation: DonationCreate,
                                     user: Optional[User] = Depends(current_user),
                                     session=session):
    """
    <h3>
        <font color="#6B7A99">Создание пожертвования.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Все пользователи.</font></p>
    """

    donation = await donation_crud.create(donation, session, user)

    return await investment_charity(donation, session)


@router.get('/my',
            response_model=List[DonationDB],
            response_model_exclude_none=True,
            summary='Просмотр своих пожертвований')
async def get_my_donation(user: User = Depends(current_user),
                          session=session):
    """
    <h3>
        <font color="#6B7A99">Просмотр всех своих пожертвований.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Авторизированный пользователь.</font></p>
    """

    return await donation_crud.get_by_user_donations(user, session)
