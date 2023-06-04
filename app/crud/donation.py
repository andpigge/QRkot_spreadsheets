from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_by_user_donations(self, user: User, session: AsyncSessionLocal):
        donations_by_user = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )

        return donations_by_user.scalars().all()


donation_crud = CRUDDonation(Donation)
