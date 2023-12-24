from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, desc, select
from sqlalchemy.dialects.mysql import match
from . import models, schemas

# def search(db: Session, arg: str, field: str):
#     return {"res":"Not found"}
Course = models.Course
def check(db: Session):
    return {"result":"Success"}

def get_full(db: Session):
    users = db.query(Course).all()
    return users

def get_partial(db: Session):
    responce = db.query(Course.rgno,Course.title_e)
    return responce

def search_limited(db: Session):
    query_list = []
    list_a = ['rgno','title_e']
    filter_list = []
    filter_list.append(Course.key for key in list_a)
    responce_list = db.query(key for key in filter_list).all()
    return responce_list