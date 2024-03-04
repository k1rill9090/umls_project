'''Модуль, содержащий настройки для подключения к бд'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import sqlite_conn


SQLALCHEMY_DATABASE_URL = sqlite_conn
# создать подключение
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Создание класса сессии (будет сессией к БД при создании объекта сессии)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# определение базовой модели
Base = declarative_base()