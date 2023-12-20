import secrets
from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import re

from . import crud, models, schemas
from .database import SessionLocal, engine

SessionClass = sessionmaker(engine)
session = SessionClass()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_current_username(
#     credentials: Annotated[HTTPBasicCredentials, Depends(security)]
# ):
#     current_username_bytes = credentials.username.encode("utf8")
#     correct_username_bytes = b"stanleyjobson"
#     is_correct_username = secrets.compare_digest(
#         current_username_bytes, correct_username_bytes
#     )
#     current_password_bytes = credentials.password.encode("utf8")
#     correct_password_bytes = b"swordfish"
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username


# @app.get("/users/me")
# def read_current_user(username: Annotated[str, Depends(get_current_username)]):
#     return {"username": username}


# /api/cataloge/v1/check
@app.get("/api/cataloge/check")
def check(db: Session = Depends(get_db)):
    return {"msg":"Welcome to ICU course API"}

# /api/cataloge/v1/auth
@app.get("/api/v1/")
def checkAPI(db: Session = Depends(get_db)):
    returm "token"


# /api/cataloge/v1/course/list
#   -token
#   -list of col
#
#   return array of json obj

# /api/cataloge/v1/course/details
#   -token
#   -regid
#   -list of col
#
#   return all data of course - syllabus (could add generated syllabus url I suppose)

# /api/cataloge/v1/course/time <- want more func. /
#   -token
#   -list of search time values
#   -match method
#   -list of cols
#
#   return list of regno

# /api/cataloge/v1/course/major
#   -token (maybe open endpoint)
#   -major
#   -list of

# /api/cataloge/v1/course/search
#   -token
#   -col to search from

# I suppose /major /search are kind of the same. request may be {"searchAgainstCols":['hogeCol','fugaCol'],"returnCols",['hekoCol','pikaCol'],"query":"pontara"}

# 単語のFuzzy Searchとかの権限は渡せないかも (DB作成のリポはあげたのとそこから機能拡張で対応はできるからチャレンジしてみるの自由)
# 同様にELAの教室情報も外部公開しないかも
# バックエンドで処理回しちゃった方がデータの転送量減って高速化するだろうから欲しい機能あればIssueでもプルリクでも気軽に

###
# /api/v1/reg_priority
#   -no_token (open info)
#   -list of wanted course
#   -year
#   -algorythm number <- regards only 1st