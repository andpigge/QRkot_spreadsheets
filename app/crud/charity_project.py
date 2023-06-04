from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(self, project_name: str,
                                     session: AsyncSessionLocal) -> Optional[int]:

        db_project_id = await session.execute(
            select(self.model.id).where(
                self.model.name == project_name
            )
        )

        return db_project_id.scalars().first()

    async def get_project_two_fields_by_id(self,
                                           project_id: int,
                                           field_one: str,
                                           field_two: str,
                                           session: AsyncSessionLocal) -> Optional[int]:

        field_one = getattr(self.model, field_one)
        field_two = getattr(self.model, field_two)

        invested = await session.execute(
            select(field_one, field_two).where(
                self.model.id == project_id
            )
        )

        return invested.first()

    async def get_projects_by_completion_rate(self,
                                              session: AsyncSessionLocal) -> list[dict[str, str, str]]:

        charity_projects = await session.execute(
            select(self.model.name,
                   self.model.create_date,
                   self.model.close_date,
                   self.model.description).where(
                       self.model.fully_invested == True)  # noqa
        )

        charity_projects = charity_projects.all()

        new_list_of_charitable_projects = []
        for charity_project in charity_projects:
            new_charity_project = {}

            donation_time = str(charity_project[2] - charity_project[1])

            new_charity_project['title'] = charity_project[0]
            new_charity_project['donation_time'] = donation_time
            new_charity_project['description'] = charity_project[3]

            new_list_of_charitable_projects.append(new_charity_project)

        return new_list_of_charitable_projects


charity_project_crud = CRUDCharityProject(CharityProject)
