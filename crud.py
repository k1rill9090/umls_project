'''Модуль, содержащий функции для работы с данными в БД'''
from sqlalchemy.sql.expression import and_
from sqlalchemy.orm import Session
from sqlalchemy import distinct
import models
import schemas
from database import SessionLocal_pubmed, SessionLocal_umls, engine_pubmed, engine_umls
import json


def get_terms(db: Session, limit: int, offset: int, id_term: int, id_art: int, term_name: str, year: str):
    '''запрос к БД в таблицу Terms, возвращает данные, отобранные по входным параметрам'''

    # в массив filters заносятся условия из параметров функции в виде объекта алхимии, который вставляется в запрос к БД
    filters = []
    if id_term != None:
        filters.append(models.Terms.id_term == id_term)
    if id_art != None:
        filters.append(models.Terms.id_art == id_art)
    if term_name != None:
        filters.append(models.Terms.term.ilike(f'%{term_name}%'))
    if year != None:
        filters.append(models.Terms.year == year)

    res = db.query(models.Terms).distinct().filter(and_(True, *filters)).limit(limit).offset(offset).all()
    # преобразование к pydantic-объекту для дальнейшей конвертации в json
    result_dto = [schemas.Terms.model_validate(row, from_attributes=True) for row in res]
    return result_dto

def get_articles(db: Session, limit: int, offset: int, id: int, title: str, year: str):
    '''запрос к БД в таблицу ArticleStruct, возвращает данные, отобранные по входным параметрам'''

    filters = []
    if title != None:
        filters.append(models.ArticleStruct.title.ilike(f'%{title}%'))
    if id != None:
        filters.append(models.ArticleStruct.id == id)
    if year != None:
        filters.append(models.ArticleStruct.year.ilike(f'%{year}%'))

    total_count = db.query(models.ArticleStruct.id).count()
    res = db.query(
        models.ArticleStruct.id,models.ArticleStruct.title,
        models.ArticleStruct.article,
        models.ArticleStruct.year).filter(and_(True, *filters)).limit(limit).offset(offset).all()
    # преобразование к pydantic-объекту для дальнейшей конвертации в json
    # result_dto = [schemas.ArticleStruct.model_validate(row, from_attributes=True) for row in res]
    arts_ans = {"meta": {"limit": limit, "offset": offset, "total_count": total_count}, "data": []}
    for i in res:
        arts_ans["data"].append({"id": i[0], "title": i[1], "article": i[2], "year": i[3]})
    return arts_ans


def get_synonyms(db: Session, limit: int, offset: int, id: int, record: str, record_synonyms: str, date_add: str, id_art: int):
    '''запрос к БД в таблицу Statistic_similar_results12, возвращает данные, отобранные по входным параметрам'''

    filters = []
    if id != None:
        filters.append(models.Statistic_similar_results.id == id)
    if record != None:
        filters.append(models.Statistic_similar_results.record.ilike(f'%{record}%'))
    if record_synonyms != None:
        filters.append(models.Statistic_similar_results.record_synonyms.ilike(f'%{record_synonyms}%'))
    if date_add != None:
        filters.append(models.Statistic_similar_results.date_add == date_add)
    if id_art != None:
        filters.append(models.Statistic_similar_results.id_art_number == id_art)


    # res_records = db.query(distinct(models.Statistic_similar_results.record)).filter(and_(True, *filters)).all()
    res_records = db.query(distinct(models.Statistic_similar_results.record)).filter(and_(True, *filters)).limit(limit).offset(offset).all()
    
    list_records = [res[0] for res in res_records]

    # список для формирования будущего json ответа
    my_resp = []
    # print(list_records)

    for list_record in list_records:
        my_resp.append({"name": list_record, "children": []})
        res_attr = db.query(
            models.Statistic_similar_results.record_synonyms,
            models.Statistic_similar_results.date_add,
            models.Statistic_similar_results.id_art_number,
            models.Statistic_similar_results.similarity_percent
            ).filter(and_(True, *filters, models.Statistic_similar_results.record == list_record)).all()
        # print(f"Записи для {list_record}:\n", res_attr)s

        # формирование json из полученных выше запросов (такая структура json нужна на вход компоненту по отрисовке графа в react)
        for attr in res_attr:
            my_resp[-1]["children"].append(
                {
                "name": attr[0].strip(''' [']" '''),
                "attributes": 
                    {
                    "date_add": attr[1],
                    "id_article": str(attr[2]),
                    "similarity_perecentage": str(attr[3])
                    }
                }
                )
    # ans_json = json.dumps(my_resp)
    return my_resp


def get_stat(db: Session, limit: int, offset: int, id_term: int, term: str, year: int):
    '''запрос к БД в таблицу StatResult, возвращает данные, отобранные по входным параметрам'''

    filters = []
    if term != None:
        filters.append(models.StatResult.term.ilike(f'%{term}%'))
    if id_term != None:
        filters.append(models.StatResult.id_term == id_term)
    if year != None:
        filters.append(models.StatResult.year == year)

    total_count = db.query(models.StatResult.id_term).count()
    res = db.query(
        models.StatResult.term, models.StatResult.stat_number,
        models.StatResult.year).filter(and_(True, *filters)).limit(limit).offset(offset).all()
    arts_ans = {"meta": {"limit": limit, "offset": offset, "total_count": total_count}, "data": []}
    for i in res:
        print(i)
        arts_ans["data"].append({"termName": i[0], "numOfAppearance": i[1], "year": i[2]})
    return arts_ans
    # return True

# для отладки (код ниже работает при ручном запуске модуля)
if __name__ == '__main__':
    with SessionLocal_pubmed.begin() as session:
        # print(get_synonyms(session, 10, 0, None, None, None, None, None))
        print(get_stat(session, 5, None, None, None, '2021'))
