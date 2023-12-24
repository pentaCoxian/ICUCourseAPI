from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select
from sqlalchemy.dialects.mysql import match
from . import models, schemas

Course = models.Course


def check(db: Session):
    return {"result":"Success"}

# TODO query text formatting
def get_full(db: Session, return_columns: str):
    if return_columns == []:
        results = db.query(Course).all()
    else:
        query_list = return_columns.strip('[]')
        print(query_list)
        stmt = (
            select(text(query_list))
        )
        results = db.execute(stmt).fetch_all()
    return results


def get_partial(db: Session):
    responce = db.query(Course.rgno,Course.title_e)
    return responce

def search_limited(db: Session):
    list_a = ['rgno','title_e']
    filter_list = []
    filter_list.append(Course.key for key in list_a)
    responce_list = db.query(key for key in filter_list).all()
    return responce_list