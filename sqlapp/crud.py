from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select, DDL, event, func, or_, and_
from sqlalchemy.dialects.mysql import match
from . import models, schemas

Course = models.Course
Syllabus = models.Syllabus
Summary = models.Summary

default_fields_course = ["rgno","season","ay","course_no","old_cno","lang","section","title_e","title_j","schedule","room","comment","maxnum","instructor","unit"]
default_fields_syllabus = ['rgno', 'ay', 'term', 'cno', 'title_e', 'title_j', 'lang', 'instructor', 'unit_e', 'koma_lecture_e', 'koma_seminar_e', 'koma_labo_e', 'koma_act_e', 'koma_int_e', 'descreption', 'descreption_j', 'goals', 'goals_j', 'content', 'content_j', 'lang_of_inst', 'pollicy', 'individual_study', 'ref', 'notes', 'schedule', 'url', 'course_rgno']

def check(db: Session):
    return {"result":"Success"}

def search_legacy(db: Session, query: str='', term:str='*', selected_fields: str='title_j,title_e,instructor,descreption,descreption_j,goals,goals_j,content,content_j,lang_of_inst,pollicy,individual_study,ref,notes,schedule'):
    selected_fields = selected_fields.split(",")
    try:
        selected_attributes = [getattr(Syllabus, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"

    if query != '':
        query = '+' + query
    if len(query)!=0 and query[-1]!=' ':
        query = query.replace(' ',' +')
    match_expr = match(
        *selected_attributes,
        against=query,
    )
    stmt = (
        select(models.Syllabus.cno,models.Syllabus.term,models.Syllabus.title_j,models.Syllabus.rgno,Syllabus.lang,models.Summary.summary_j,models.Summary.summary_e)
        .filter(models.Syllabus.term.in_(['Spring Term','Autumn Term','Winter Term']) if term == '*' else models.Syllabus.term ==  term)
        .where(match_expr.in_boolean_mode())
        .order_by(desc(match_expr))
        .select_from(models.Syllabus)
        .join(models.Summary, models.Syllabus.rgno == models.Summary.rgno)  
    )
    return db.execute(stmt)


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

def search_course_with_time(db:Session, selected_fields: str, koma: str = '"3/TU","2/TH","3/TH"', query: str = '', strict: str= "complite"):
    selected_fields = selected_fields.split(",")
    try:
        selected_attributes = [getattr(Course, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    match_expr = match(
        *selected_attributes,
        against=query,
    )
    koma = koma.replace("'",'')
    times = koma.split(',')
    selected = select(Course,Syllabus)
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

def search_syllabus_with_time(db:Session, selected_fields: str, koma: str = '"3/TU","2/TH","3/TH"', query: str = '', strict: str= "complite"):
    selected_fields = selected_fields.split(",")
    try:
        selected_attributes = [getattr(Syllabus, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    match_expr = match(
        *selected_attributes,
        against=query,
    )
    koma = koma.replace("'",'')
    times = koma.split(',')
    selected = select(Syllabus, Course)
    if strict == "complite":
        # only matches complete match of koma list
        cleaned_list = [element.replace('"', '') for element in times]
        filter_time = selected.filter(Course.schedule_meta == cleaned_list)
    elif strict == "strict":
        # has to contain every koma
        filter_time = selected.filter(
                and_(*[func.JSON_CONTAINS(Course.schedule_meta, time) for time in times])
            )
    else:
        # if any of one koma matches
        filter_time = selected.filter(
                or_(*[func.JSON_CONTAINS(Course.schedule_meta, time) for time in times])
            )
    if query == '':
        stmt = (
            filter_time
            .join(Syllabus, Course.rgno == Syllabus.course_rgno)
        )
    else:
        stmt = (
            filter_time
            .join(Syllabus, Course.rgno == Syllabus.course_rgno)
            .where(match_expr.in_boolean_mode())
            .order_by(desc(match_expr))
        )
    return db.execute(stmt)


def search_syllabus_with_time2(db:Session, selected_fields: str, koma: str = '"3/TU","2/TH","3/TH"', query: str = '', strict: str= "complite"):
    search_term = "asia"
    query = db.query(Syllabus, Course).join(Syllabus, Course.rgno == Syllabus.course_rgno).filter(
        text("MATCH(syllabi.title_j,syllabi.title_e) AGAINST(:search_term IN BOOLEAN MODE)").bindparams(search_term=search_term)
    )
    
    return query.all()

def makeFullTextIndex(db: Session, tablename: str = 'courses', indexname: str = "idx_title", field: str = "title_j, title_e"):
    sql = """ALTER TABLE """ + tablename + """ ADD FULLTEXT INDEX IF NOT EXISTS """ + indexname +  """(""" + field + """) COMMENT 'tokenizer "TokenMecab"';"""
    print(sql)
    db.execute(text(sql))
    db.flush()

def getById(db: Session, id: str):
    stmt=select(Syllabus.ay,
            Syllabus.rgno,
            Syllabus.ay,
            Syllabus.term,
            Syllabus.cno,
            Syllabus.title_e ,
            Syllabus.title_j ,
            Syllabus.lang ,
            Syllabus.instructor,
            Syllabus.unit_e ,
            Syllabus.koma_lecture_e ,
            Syllabus.koma_seminar_e ,
            Syllabus.koma_labo_e,
            Syllabus.koma_act_e,
            Syllabus.koma_int_e ,
            Syllabus.descreption,
            Syllabus.descreption_j,
            Syllabus.goals,
            Syllabus.goals_j,
            Syllabus.content,
            Syllabus.content_j,
            Syllabus.lang_of_inst,
            Syllabus.pollicy,
            Syllabus.individual_study,
            Syllabus.ref ,
            Syllabus.notes ,
            Syllabus.schedule ,
            Course.section,
            Course.maxnum,
            Course.room).where(Syllabus.rgno == int(id)).join(Syllabus,Syllabus.rgno == Course.rgno)
    
    return db.execute(stmt)