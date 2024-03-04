from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import crud, models, schemas
from database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='REST API for UMLS database')
# установка CORS в заголовках ответа (для избежания CORS блокировки апи в браузере)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/terms", response_model=list[schemas.Terms])
def get_terms(
    limit: int = 10, offset: int = 0,
    term_name: str = None, id_term: int = None, 
    id_art: int = None,
    year: str = None, 
    db: Session = Depends(get_db)
    ):

    terms = crud.get_terms(db, limit, offset, id_term, id_art, term_name, year)
    if terms is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return terms

@app.get("/articles", response_model=schemas.ArticleStruct)
def get_articles(
    limit: int = 5, offset: int = 0,
    db: Session = Depends(get_db)
    ):

    articles = crud.get_articles(db, limit, offset)
    if articles is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return articles

@app.get("/synonyms", response_model=list[schemas.Synonims_terms])
def get_synonyms(
    limit: int = 10, offset: int = 0, 
    id: int = None, record: str = None, 
    record_synonyms: str = None,
    date_add: str = None,
    id_art: int = None,
    db: Session = Depends(get_db)
    ):

    syns = crud.get_synonyms(db, limit, offset, id, record, record_synonyms, date_add, id_art)
    if syns is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return syns

# Запуск сервера: uvicorn main:app --reload
# Команда uvicorn main:app ссылается на:
# * main: файл main.py (модуль Python).
# * app: объект, созданный внутри main.py на строке app = FastAPI().
# * --reload: перезагружает сервер при изменениях кода. Используется только для разработки.
# http://127.0.0.1:8000/docs - автоматически генерируемая документация по api
# http://127.0.0.1:8000/redoc - альтернативный вариант документации

