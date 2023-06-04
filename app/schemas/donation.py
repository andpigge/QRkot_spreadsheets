from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationBaseAbstract(BaseModel):
    __abstract__ = True

    full_amount: int = Field(...,
                             gt=1,
                             description='Требуемая сумма',
                             example=2000)
    comment: Optional[str]

    def __repr__(self):
        return f'Требуемая сумма: {self.full_amount}, {self.comment[:10]}'


class DonationCreate(DonationBaseAbstract):

    class Config:
        title = 'Request body - создать пожертвования'


class DonationGetAllDB(DonationBaseAbstract):
    id: int = Field(..., example=1)
    user_id: Optional[int] = Field(example=1)
    invested_amount: int = Field(..., description='Сумма из пожертвования')
    fully_invested: bool = Field(..., description='Все ли деньги из пожертвования были переведены в тот или иной проект')
    create_date: datetime = Field(...,
                                  description='Дата пожертвования')
    close_date: Optional[datetime] = Field(..., description='Дата закрытия проекта. Момент набора нужной суммы')

    class Config:
        title = 'Response получить все пожертвования'
        orm_mode = True


class DonationDB(DonationBaseAbstract):
    id: int = Field(..., example=1)
    create_date: datetime = Field(...,
                                  description='Дата пожертвования')

    class Config:
        title = 'Response пожертвования'
        orm_mode = True
