'''Модуль, содержащий настройки для подключения к бд'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import sqlite_conn_umls, sqlite_conn_pubmed


SQLALCHEMY_DATABASE_UMLS_URL = sqlite_conn_umls
SQLALCHEMY_DATABASE_PUBMED_URL = sqlite_conn_pubmed
# создать подключение
engine_umls = create_engine(
    SQLALCHEMY_DATABASE_UMLS_URL, connect_args={"check_same_thread": False}
)
# Создание класса сессии (будет сессией к БД при создании объекта сессии, т.е. для каждого вызова апи создается отдельная сессия)
# строка ниже для подключения к БД PubMedArticles-7_umls.db
SessionLocal_umls = sessionmaker(autocommit=False, autoflush=False, bind=engine_umls)

# строки ниже для подключения к БД PubMedArticles-7.db
engine_pubmed = create_engine(
    SQLALCHEMY_DATABASE_PUBMED_URL, connect_args={"check_same_thread": False}
)
SessionLocal_pubmed = sessionmaker(autocommit=False, autoflush=False, bind=engine_pubmed)

# определение базовой модели
Base = declarative_base()