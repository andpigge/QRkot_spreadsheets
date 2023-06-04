from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(project_name: str,
                               session: AsyncSession) -> None:

    room_id = await charity_project_crud.get_project_id_by_name(project_name, session)

    if room_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(charity_project_id: int,
                                       session: AsyncSession) -> CharityProject:

    charity_project = await charity_project_crud.get(charity_project_id, session)

    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Благотворительный проект не найден!'
        )

    return charity_project


async def check_closed_invested_project(charity_project_id: int,
                                        session: AsyncSession) -> CharityProject:

    fully_invested, invested_amount = await charity_project_crud.get_project_two_fields_by_id(charity_project_id,
                                                                                              'fully_invested',
                                                                                              'invested_amount',
                                                                                              session)

    if fully_invested is True or invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_closed_update_project(charity_project_id: int,
                                      obj_in: CharityProjectUpdate,
                                      session: AsyncSession) -> CharityProject:

    fully_invested, invested_amount = await charity_project_crud.get_project_two_fields_by_id(charity_project_id,
                                                                                              'fully_invested',
                                                                                              'invested_amount',
                                                                                              session)

    if fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )

    if obj_in.full_amount and obj_in.full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail=f'Нельзя установить сумму меньше уже внесенной: {invested_amount}'
        )
