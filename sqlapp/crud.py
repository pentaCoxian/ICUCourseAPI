from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select, DDL, event, func, or_, and_
from sqlalchemy.dialects.mysql import match
from . import models, schemas

Course = models.Course
Syllabus = models.Syllabus

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
def search_by_time(db: Session, selected_fields: str, qery: str):
    if qery != '':
        qery = '+' + qery
    if len(qery)!=0 and qery[-1]!=' ':
        qery = qery.replace(' ',' +')
    try:
        selected_fields = selected_fields.split(",")
        selected_attributes = [getattr(Course, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    match_expr = match(
            *selected_attributes,
            against=qery,
    )
    stmt = (
        select('*')
        .where(match_expr.in_boolean_mode())
        .order_by(desc(match_expr))
    )
    return db.execute(stmt)
    # return match_expr

def experimental(db:Session, selected_fields: str, koma: str = '"3/TU","2/TH","3/TH"', query: str = '', strict: str= "complite"):
    selected_fields = selected_fields.split(",")
    selected_attributes = [getattr(Course, field) for field in selected_fields]
    match_expr = match(
        *selected_attributes,
        against=query,
    )
    koma = koma.replace("'",'')
    times = koma.split(',')
    selected = select(Course,Syllabus)
    print(times)
    if strict == "complite":
        # only matches complete match of koma list
        cleaned_list = [element.replace('"', '') for element in times]
        filter_time = selected.filter(Course.schedule_meta == cleaned_list)
    elif strict == "strict":
        # has to contain every koma
        filter_time = selected.filter(
                and_(*[func.JSON_CONTAINS(Course.schedule_meta, time) for time in times])
            )
    elif strict == "loose":
        # if any of one koma matches
        filter_time = selected.filter(
                or_(*[func.JSON_CONTAINS(Course.schedule_meta, time) for time in times])
            )
    if query == '':
        stmt = (
            filter_time
            .join(Course, Course.rgno == Syllabus.course_rgno)
        )
    else:
        stmt = (
            filter_time
            .join(Course, Course.rgno == Syllabus.course_rgno)
            .where(match_expr.in_boolean_mode())
            .order_by(desc(match_expr))
        )
    return db.execute(stmt)

def makeFullTextIndex(db: Session, tablename: str = 'courses', indexname: str = "idx_title", field: str = "title_j, title_e"):
    sql = """ALTER TABLE """ + tablename + """ ADD FULLTEXT INDEX IF NOT EXISTS """ + indexname +  """(""" + field + """) COMMENT 'tokenizer "TokenMecab"';"""
    return db.execute(text(sql))


string = '"4/M","4/W"'
string.split(',')