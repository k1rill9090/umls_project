'''Модуль, который обращается к таблице Terms'''

from sqlalchemy import create_engine, text, select, MetaData
from config import sqlite_conn
from models import Terms


# создать подключение
engine = create_engine(
    url=sqlite_conn
    # echo=True,
    # pool_size=5,
    # max_overflow=10
)

# контекстный менеджер with сам закрывает подключение по окончанию
with engine.connect() as conn:
    # res = conn.execute(select(Terms).limit(1).offset(None))
    res = conn.query(Terms).limit(1).offset(None)
    print(res.all())
