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

@app.get("/api/v2/legacy")
def legacy(query:str = "",term:str="", db: Session = Depends(get_db)):
    db_responce = crud.search_legacy(db, query, term).mappings().all()
    resultDictList=[]
    for i in db_responce:
        tmp = dict(i)
        if tmp['lang']== "":
            tmp['lang']= "TBA"
        resultDictList.append(tmp)
    return resultDictList

@app.get("/api/v2/details")
def getdetailsWithInfo(id:str,db: Session = Depends(get_db)):
    result = crud.getById(db,id=id).mappings().all()
    print(result)
    resultDictList=[]
    for i in result:
        tmp = dict(i)
        resultDictList.append(tmp)
    return resultDictList[0]


# # /api/cataloge/v1/auth
# @app.get("/api/v1/auth")
# def checkAPI(db: Session = Depends(get_db)):
#     return {"msg":"Welcome to ICU course API"}
# For now, token verification will not be used. instead nginx will filter non whi
@app.get("/api/v2/auth", status_code = 501)
def generate_token(db: Session = Depends(get_db)):
    return {"msg": "not implimented","token":""}

@app.get("/api/v2/course/list")
def course_full(db: Session = Depends(get_db), returns: str = 'rgno,title_e'):
    db_responce = crud.search_limited(db, returns)
    responce = {}
    responce["responce"] = db_responce
    return responce

@app.get("/api/v2/course/search")
def search_from_target(db: Session = Depends(get_db), returns: str = 'rgno,title_e', target: str = 'rgno,title_e', query: str = ''):
    db_responce = crud.search(db, returns, target, query)
    responce = {}
    responce["responce"] = db_responce
    
@app.get("/api/v2/full/search")
def search_from_full(db: Session = Depends(get_db), returns: str = 'rgno,title_e', schedule: str = '1M', query: str = ''):
    db_responce = crud.search(db, returns, schedule, query)
    responce = {}
    responce["responce"] = db_responce
    
@app.get("/api/v2/time/course")
def course_from_time(db: Session = Depends(get_db), target: str = 'title_j,title_e', query: str = '', koma: str = '"3/TU"', strict: str = 'strict'):
    indexname = target.replace("'",'').replace(',','_')
    crud.makeFullTextIndex(db, tablename = 'courses', indexname = indexname+'_idx', field = target)
    db_responce = crud.search_course_with_time(db, selected_fields = target, koma = koma, query = query, strict = strict)
    dictLis = []
    for row in db_responce:
        row_as_dict = row._asdict()
        dictLis.append(row_as_dict)
    return dictLis

@app.get("/api/v2/time/syllabus")
def syllabus_from_time(db: Session = Depends(get_db), target: str = 'title_j,title_e,instructor,descreption,descreption_j,goals,goals_j,content,content_j,lang_of_inst,pollicy,individual_study,ref,notes,schedule', query: str = '', koma: str = '"3/TU"', strict: str = 'strict'):
    # TODO
    # make the index generation automated. Currently needs to be generated by hand   
    db_responce = crud.search_syllabus_with_time(db, selected_fields = target, koma = koma, query = query, strict = strict)
    dictLis = []
    for row in db_responce:
        row_as_dict = row._asdict()
        dictLis.append(row_as_dict)
    return dictLis

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