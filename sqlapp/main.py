from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import re

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Cors will be added by nginx
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,   # 追記により追加
#     allow_methods=["*"],      # 追記により追加
#     allow_headers=["*"]       # 追記により追加
# )
# regno ay term cno title_e  title_j  lang  instructor unit_e  koma_lecture_e  koma_seminar_e  koma_labo_e koma_act_e koma_int_e  descreption descreption_j goals goals_j content content_j lang_of_inst pollicy individual_study ref  notes  schedule 

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# /api/cataloge/v1/check
@app.get("/api/cataloge/check")
def check(db: Session = Depends(get_db)):
    return {"msg":"Welcome to ICU course API"}

# /api/cataloge/v1/auth
@app.get("/api/v1/")
def 


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







# @app.get("/api/v1/search/")
# def search_full(q:str = "",term:str="", db: Session = Depends(get_db)):
#     result = crud.fullTextSearch(db,arg=q,field="ay, term, cno, title_e, title_j, lang, instructor, unit_e, koma_lecture_e, koma_seminar_e, koma_labo_e, koma_act_e, koma_int_e, descreption, descreption_j, goals, goals_j, content, content_j, lang_of_inst, pollicy, individual_study, ref, notes, schedule")
#     dictLis = []
#     for row in result:
#         row_as_dict = row._asdict()
#         dictLis.append(row_as_dict)
#     return dictLis

# @app.get("/api/v1/init/")
# def make_index(db: Session = Depends(get_db)):
#     return crud.makeFullTextIndex(db,"syllabuses",'nourl','ay, term, cno, title_e, title_j, lang, instructor, unit_e, koma_lecture_e, koma_seminar_e, koma_labo_e, koma_act_e, koma_int_e, descreption, descreption_j, goals, goals_j, content, content_j, lang_of_inst, pollicy, individual_study, ref, notes, schedule')

# # Same as search but not using raw sql(working)
# @app.get("/api/v1/beta/")
# def search_beta(q:str = "",term:str="",db: Session = Depends(get_db)):
#     result = crud.betaMatch(db,q=q,term=term).mappings().all()
#     return result

# # Makes fulltext index if not exists(slower but won't err out)
# @app.get("/api/v1/search-v2/")
# def searchV2(q:str = "",term:str="",db: Session = Depends(get_db)):
#     result = crud.robustFullTextSearch(db,arg="日本 社会",field="title_j, title_e, content_j")
#     dictLis = []
#     for row in result:
#         row_as_dict = row._asdict()
#         dictLis.append(row_as_dict)
#     return dictLis

# # fetch by id (OK working)
# @app.get("/api/v1/details/")
# def searchFromID(id:str,db: Session = Depends(get_db)):
#     result = crud.searchFromID(db,id=id)[0].__dict__
#     result = dict(result)
#     result.pop('_sa_instance_state')
#     for k,v in result.items():
#         result[k] = re.sub(r'\n+', '\n', str(v)).strip()
#     print(result)
#     return result

# @app.get("/api/v2/search-top")
# def searchTop(q:str = "",term:str="",db: Session = Depends(get_db)):
#     result = crud.searchTop(db,q=q,term=term).mappings().all()
#     return result

# @app.get("/api/v2/search-snippet")
# def getSnippet(q:str = "",term:str="",db: Session = Depends(get_db)):
#     result = crud.betaMatch(db,q=q,term=term).mappings().all()
#     resultDictList =[]
#     for i in result:
#         tmp = dict(i)
#         appendDict ={}
#         appendDict.update({
#             'cno':tmp['cno'],
#             'term':tmp['term'],
#             'title_j':tmp['title_j'],
#             'title_e':tmp['title_e'],
#             'regno':tmp['regno'],
#         })
#         for e in ['ay','term','cno','title_e','title_j','regno','ref']:
#             tmp.pop(e)
#         dictValues = str(tmp.values())
#         dictValues = re.sub(r'\n+', '\n', dictValues).strip()
#         valueList = re.split(r'(\.|。|\', \'| \')|\\n',dictValues)
#         resultList = []
#         for n in valueList:
#             if n == None or len(n) < 3 :
#                 pass
#             else: 
#                 for f in q.strip().split(' '):
#                     if len(re.findall(f,n))>0:
#                         n = re.sub(r'\\\\n+', '', n).strip()
#                         n = re.sub(r'\\n+', '', n).strip()
#                         resultList.append(n)
    
#         appendDict['hits'] = resultList
#         appendDict['htnum'] = len(resultList)
#         resultDictList.append(appendDict)
#     resultDictList = sorted(resultDictList,key=lambda x:x['htnum'],reverse=True)
#     return resultDictList

# @app.get("/api/v3/search")
# def getSnippet(q:str = "",term:str="",db: Session = Depends(get_db)):
#     result = crud.sigmaMatch(db,q=q,term=term).mappings().all()
#     resultDictList=[]
#     for i in result:
#         tmp = dict(i)
#         resultDictList.append(tmp)
#     return resultDictList

