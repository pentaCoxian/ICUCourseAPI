from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select
from sqlalchemy.dialects.mysql import match
from . import models, schemas

Course = models.Course

default_fields = ["rgno","season","ay","course_no","old_cno","lang","section","title_e","title_j","schedule","room","comment","maxnum","instructor","unit"]

def check(db: Session):
    return {"result":"Success"}


def search_limited(db: Session, selected_fields: str):
    selected_fields = selected_fields.strip("[]").split(",")
    try:
        selected_attributes = [getattr(Course, field) for field in selected_fields]
    except AttributeError as err:
        return str(err)
    except:
        return "Internal error"
    query_result = db.query(*selected_attributes).all()
    responce_list= [dict(zip(selected_fields, row)) for row in query_result]
    return responce_list