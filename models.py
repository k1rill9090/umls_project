'''Модуль, содержащий модели бд для выполнения запросов через ORM'''
from sqlalchemy import Column, Integer, String, Float
from database import Base


class Terms(Base):
    __tablename__ = "Terms"
    id_term = Column(name="idTerm", type_=Integer, primary_key=True)
    term = Column(name="term", type_=String)
    id_art = Column(name="idArt", type_=Integer)
    year = Column(type_=String)

class Statistic_similar_results(Base):
    __tablename__ = "Statistic_similar_results12"

    id = Column(name="id", type_=Integer, primary_key=True)
    record = Column(name="record", type_=String)
    record_synonyms = Column(name="record_synonyms", type_=String)
    date_add = Column(name="date_add", type_=String)
    id_art_number = Column(name="idArt_number", type_=Integer)
    similarity_percent = Column(name="similarity_percentage", type_=Float)

class ArticleStruct(Base):
    __tablename__ = "ArticleStruct"

    id = Column(name="idArt", type_=Integer, primary_key=True)
    author = Column(name="Author", type_=String)
    title = Column(name="Title", type_=String)
    article = Column(name="Abstract", type_=String)
    year = Column(name="Year", type_=String)
