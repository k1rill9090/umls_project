'''Модуль, содержащий схемы Pydantic (для создания и валидации структуры REST API)'''
from pydantic import BaseModel, Field, field_validator, FieldValidationInfo, validator
from datetime import date
import re

class Terms(BaseModel):
    '''схема для валидации ответа метода GET /terms'''
    id_term: int
    term: str
    id_art: int
    year: str
    # class Config:
    #     orm_mode = True

class Synonims_terms(BaseModel):
    '''схема для валидации ответа метода GET /synonyms'''
    name: str
    children: list[dict]

class ArticleStruct(BaseModel):
    '''схема для валидации ответа метода GET /articles'''

    meta: dict
    data: list[dict]
    # class Config:
    #     orm_mode = True
    
class StatResult(BaseModel):
    '''схема для валидации ответа метода GET /statistics'''
    
    # meta: dict
    # data: list
    termName: str
    numOfAppearance: int
    year: str

class AddAbstracts(BaseModel):
    '''схема для валидации пейлоада метода POST /articles'''

    count_articles: int = Field(ge=1, le=100)
    keywords: str
    start_date: date
    
    @field_validator("start_date")
    def check_date_range(cls, value: date, info: FieldValidationInfo) -> date:
    
        if value < date(1900, 1, 1):
            # Raise a ValueError with the error message
            raise ValueError("Start date must be greater than 1900.01.01")
        return value

    end_date: date
    
    @field_validator("end_date")
    def ensure_date_range(cls, value: date, info: FieldValidationInfo) -> date:
        start_date = info.data.get("start_date", None)
        # если дата меньше 1900 года, то значение переменной = none, 
        # из-за чего при запуске этого валидатора появляется ошибка сравнения переменных
        if start_date != None and value < start_date:
            # Raise a ValueError with the error message
            raise ValueError("End date must be greater than the start date.")
        return value
    
    @validator("keywords")
    def check_search_string(cls, value: str) -> str:
        if not re.match(r'^[a-zA-Z\s\d-]{1,}$', value):
            # Raise a ValueError with the error message
            raise ValueError("Searching string must have latin symbols, digits, spaces and dashes")
        return value

