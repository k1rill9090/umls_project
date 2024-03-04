'''Модуль, содержащий схемы Pydantic (для создания и валидации структуры REST API)'''
from pydantic import BaseModel


class Terms(BaseModel):
    id_term: int
    term: str
    id_art: int
    year: str
    # class Config:
    #     orm_mode = True

class Synonims_terms(BaseModel):
    name: str
    children: list[dict]

class ArticleStruct(BaseModel):
    meta: dict
    data: list[dict]
    # class Config:
    #     orm_mode = True


