from sqlalchemy.orm import Session
from sqlalchemy import text, desc, select
from sqlalchemy.dialects.mysql import match
from . import models, schemas

def search(db: Session, arg: str, field: str):
    return