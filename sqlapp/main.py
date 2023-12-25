from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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
 
# /api/cataloge/v1/check
# Just to check if API is alive
@app.get("/api")
def check_API(db: Session = Depends(get_db)):
    return {"msg":"Welcome to ICU course API"}

# # /api/cataloge/v1/auth
# @app.get("/api/v1/auth")
# def checkAPI(db: Session = Depends(get_db)):
#     return {"msg":"Welcome to ICU course API"}
# For now, token verification will not be used. instead nginx will filter non whi
@app.get("/api/c/v1/auth", status_code = 501)
def generate_token(db: Session = Depends(get_db)):
    return {"msg": "not implimented","token":""}

@app.get("/api/c/v1/course/list")
def course_full(db: Session = Depends(get_db), returns: str = 'rgno,title_e'):
    db_responce = crud.search_limited(db, returns)
    responce = {}
    responce["responce"] = db_responce
    return responce

@app.get("/api/c/v1/course/search")
def search_from_target(db: Session = Depends(get_db), returns: str = 'rgno,title_e', target: str = 'rgno,title_e', query: str = ''):
    db_responce = crud.search(db, returns, target, query)
    responce = {}
    responce["responce"] = db_responce
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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ICU API",
        version="v0.5.0",
        summary="This is is based on OpenAPI schema",
        description="All data acessable are taken from data available to the public.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi