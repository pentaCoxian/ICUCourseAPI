from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import re
import os
from . import crud, models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import sessionmaker


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@app.get("/")
def check_root():
    return {"hello":"api"}


# /api/cataloge/v1/check
# Just to check if API is alive
@app.get("/api/check")
def checkAPI(db: Session = Depends(get_db)):
    return {"msg":"Welcome to ICU course API"}

# # /api/cataloge/v1/auth
# @app.get("/api/v1/auth")
# def checkAPI(db: Session = Depends(get_db)):
#     return {"msg":"Welcome to ICU course API"}
# For now, token verification will not be used. instead nginx will filter non whi
@app.get("/api/c/v1/auth", status_code = 501)
def generateToken(db: Session = Depends(get_db)):
    return {"msg": "not implimented","token":""}

# /api/cataloge/v1/course/list
#   -token
#   -list of col
#
#   return array of json obj
@app.get("/api/c/v1/course/fulllist")
def Course_full(ids = '30307',db: Session = Depends(get_db)):
    db_responce = crud.get_full(db)
    # responce = []
    # for row in db_responce:
    #     row_as_dict = row._asdict()
    #     responce.append(row_as_dict)
    responce = db_responce
    return {"responce":responce}

@app.get("/api/c/v1/course/partial")
def Course_full(db: Session = Depends(get_db)):
    db_responce = crud.get_partial(db)
    responce = db_responce
    return {"responce":responce}

@app.get("/api/c/v1/course/list")
def Course_full(db: Session = Depends(get_db)):
    db_responce = crud.search_limited(db,responce_columns)
    responce = db_responce
    return {"responce":responce}

# /api/cataloge/v1/course/course/details
#   -token
#   -regid
#   -list of col
#
#   return all data of course - syllabus (could add generated syllabus url I suppose)
# @app.get("/api/cataloge/v1/course/course/details")
# async def create_item(item: schemas.Item):
#     return item

# @app.get("/api/c/v1/course/details")
# def search_details(dv: Session = Depends(get_db)):
#     res = crud.search_from_id( ids = "30307", Session = Session)
#     return res


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