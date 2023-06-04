from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectBaseAbstract(BaseModel):
    __abstract__ = True

    name: Optional[str] = Field(max_length=100,
                                description='Можно вводить в любом регистре',
                                example='Вкусный корм')
    description: Optional[str] = Field(description='Можно вводить в любом регистре',
                                       example='Вкусный корм фирмы \'Кис-Кис-Мяу\'')
    full_amount: Optional[int] = Field(gt=1,
                                       description='Требуемая сумма',
                                       example=2000)

    def __repr__(self):
        return f'{self.name}, {self.description[:10]}, требуемая сумма: {self.full_amount}'

    class Config:
        min_anystr_length = 1


class CharityProjectDB(CharityProjectBaseAbstract):
    id: int = Field(..., example=1)
    invested_amount: int = Field(..., description='Внесённая сумма')
    fully_invested: bool = Field(..., description='Собрана ли нужная сумма для проекта (закрыт ли проект)')
    create_date: datetime = Field(...,
                                  description='Дата создания проекта')
    close_date: Optional[datetime] = Field(description='Дата закрытия проекта. Момент набора нужной суммы')

    class Config:
        title = 'Response благотворительные проекты'
        orm_mode = True


class CharityProjectCreate(CharityProjectBaseAbstract):
    name: str = Field(...,
                      max_length=100,
                      example='Вкусный корм',
                      exclude={'name'})
    description: str = Field(...,
                             example='Вкусный корм фирмы \'Кис-Кис-Мяу\'')
    full_amount: int = Field(...,
                             gt=1,
                             example=2000)

    class Config:
        title = 'Request body - создание благотворительного проекта'


class CharityProjectUpdate(CharityProjectBaseAbstract):

    class Config:
        title = 'Request body - обновление благотворительного проекта'
        extra = Extra.forbid
