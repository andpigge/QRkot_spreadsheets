from sqlalchemy import Column, String, Text

from app.core.generals_abstract_models import CharityAbstract


class CharityProject(CharityAbstract):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
