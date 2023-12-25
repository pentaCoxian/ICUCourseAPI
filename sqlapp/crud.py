from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select
from sqlalchemy.dialects.mysql import match
from . import models, schemas

Course = models.Course

default_fields = ["rgno","season","ay","course_no","old_cno","lang","section","title_e","title_j","schedule","room","comment","maxnum","instructor","unit"]

def check(db: Session):
    return {"result":"Success"}


def search_limited(db: Session, selected_fields: str):
    selected_fields = selected_fields.split(",")
    try:
        selected_attributes = [getattr(Course, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    query_result = db.query(*selected_attributes).all()
    responce_list= [dict(zip(selected_fields, row)) for row in query_result]
    return responce_list

def search(db: Session, selected_fields: str, target: str, query: str):
    selected_fields = selected_fields.split(",")
    query = query.split(",")
    
    query_filters = []
    for column, condition in zip(selected_fields, conditions):
        query_filters.append(or_(getattr(Course, column) == c for c in condition.split(',')))
    query = db.query(Course).filter(and_(*query_filters))
   
# TODO
# add schedule filter
def search_by_time(db: Session, qery: str, term:str):
    if qery != '':
        qery = '+' + qery
    if len(qery)!=0 and qery[-1]!=' ':
        qery = qury.replace(' ',' +')
    try:
        selected_attributes = [getattr(Course, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    match_expr = match(
            *selected_attributes,
            against=q,
    )

    stmt = (
        select('*')
        .filter(Course.term.in_(['Spring Term','Autumn Term','Winter Term']) if term == '*' else models.Course.term ==  term)
        .filter(Course.schedule)
        .where(match_expr.in_boolean_mode())
        .order_by(desc(match_expr))
    )
    return db.execute(stmt)
