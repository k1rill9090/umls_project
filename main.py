from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import crud, models, schemas
from database import SessionLocal_pubmed, SessionLocal_umls, engine_umls, engine_pubmed
from CreateCorpus.CreateCorpus import create_corpus
from CreateCorpus.Tokenize_text import TokenizeText
from CreateCorpus.Stat import Statistics
import check_delete_db



# models.Base.metadata.create_all(bind=engine)
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
def get_db_umls():
    db = SessionLocal_umls()
    try:
        yield db
    finally:
        db.close()

def get_db_pubmed():
    db = SessionLocal_pubmed()
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
    db: Session = Depends(get_db_pubmed)
    ):

    terms = crud.get_terms(db, limit, offset, id_term, id_art, term_name, year)
    if terms is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return terms

@app.get("/articles", response_model=schemas.ArticleStruct)
def get_articles(
    id: int = None, title: str = None, year: str = None,
    limit: int = 5, offset: int = 0,
    db: Session = Depends(get_db_pubmed)
    ):

    articles = crud.get_articles(db, limit, offset, id, title, year)
    if articles is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return articles

@app.get("/statistics", response_model=schemas.ArticleStruct)
def get_terms_statistics(
    id_term: int = None, term_name: str = None, year: str = None,
    limit: int = 5, offset: int = 0,
    db: Session = Depends(get_db_pubmed)
    ):

    stat = crud.get_stat(db, limit, offset, id_term, term_name, year)
    if stat is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return stat

@app.get("/synonyms", response_model=list[schemas.Synonims_terms])
def get_synonyms(
    limit: int = 10, offset: int = 0, 
    id: int = None, record: str = None, 
    record_synonyms: str = None,
    date_add: str = None,
    id_art: int = None,
    db: Session = Depends(get_db_umls)
    ):

    syns = crud.get_synonyms(db, limit, offset, id, record, record_synonyms, date_add, id_art)
    if syns is None:
        raise HTTPException(status_code=404, detail="Terms not found")
    return syns

@app.post("/articles")
def add_abstracts(params: schemas.AddAbstracts):
    try:
        create_corpus(params.count_articles, params.keywords, params.start_date, params.end_date)
    except Exception as exp:
        print(exp)
        raise HTTPException(500, str(exp))
    return({"code": 200, "message": "Данные успешно загружены"})

@app.post("/terms")
def find_terms():
    try:
        TokenizeText.Tokenize_text()
    except Exception as exp:
        print(exp)
        raise HTTPException(500, str(exp))
    return({"code": 200, "message": "Выделение терминов выполнео успешно"})

@app.post("/statistics")
def calc_terms():
    try:
        Statistics.statistics()
    except Exception as exp:
        print(exp)
        raise HTTPException(500, str(exp))
    return({"code": 200, "message": "Расчет статистики встречаемости терминов выполнен успешно"})

@app.delete("/clearPubmedArticles")
def clear_db():
    try:
        check_delete_db.clear_db()
    except Exception as exp:
        print(exp)
        raise HTTPException(500)
    return({"message": "Все таблицы очищены"})



# Запуск сервера: uvicorn main:app --reload
# Команда uvicorn main:app ссылается на:
# * main: файл main.py (модуль Python).
# * app: объект, созданный внутри main.py на строке app = FastAPI().
# * --reload: перезагружает сервер при изменениях кода. Используется только для разработки.
# http://127.0.0.1:8000/docs - автоматически генерируемая документация по api
# http://127.0.0.1:8000/redoc - альтернативный вариант документации

