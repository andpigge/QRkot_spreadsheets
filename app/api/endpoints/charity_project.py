from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_closed_invested_project,
                                check_closed_update_project,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment_charity import investment_charity

router = APIRouter()

session: AsyncSession = Depends(get_async_session)


@router.get('/',
            response_model=List[CharityProjectDB],
            response_model_exclude_none=True,
            summary='Все благотворительные проекты')
async def get_all_charity_projects(session=session):
    """
    <h3>
        <font color="#6B7A99">Получение всех благотворительных проектов.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Все пользователи.</font></p>
    """

    return await charity_project_crud.get_multi(session)


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],
             summary='Создание благотворительного проекта')
async def create_new_charity_project(charity_project: CharityProjectCreate,
                                     session=session):
    """
    <h3>
        <font color="#6B7A99">Создание благотворительного проекта.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Суперпользователь.</font></p>
    """

    await check_name_duplicate(charity_project.name, session)

    new_room = await charity_project_crud.create(charity_project, session)

    return await investment_charity(new_room, session)


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)],
              summary='Обновление благотворительного проекта')
async def update_reservation(project_id: int,
                             obj_in: CharityProjectUpdate,
                             session=session):
    """
    <h3>
        <font color="#6B7A99">Обновление благотворительного проекта.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Суперпользователь.</font></p>
    <h4>Обновление доступно для полей:</h4>

    - name (Имя)
    - description (Описание)
    - full_amount (Требуемая сумма)
    """

    charity_project = await check_charity_project_exists(project_id, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    await check_closed_update_project(project_id, obj_in, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )

    return charity_project


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)],
               summary='Удаление благотворительного проекта')
async def remove_meeting_room(project_id: int,
                              session: AsyncSession = Depends(get_async_session)):
    """
    <h3>
        <font color="#6B7A99">Удаление благотворительного проекта.</font>
    </h3>
    <p><font color="#EB5757">Права доступа: Суперпользователь.</font></p>
    """

    await check_closed_invested_project(project_id, session)

    charity_project = await check_charity_project_exists(project_id, session)

    return await charity_project_crud.remove(charity_project, session)
