#code to make a summary table in database

import os
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select, Text, JSON, Boolean
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
from openai import OpenAI
import os
from langdetect import detect
import re
import json
import time
from tqdm import tqdm

#load env variables
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

#make engine
engine = sa.create_engine(os.environ['MARIADB_ADDRESS'],echo=False)
Base = declarative_base()

#course orm

class Course(Base):
    __tablename__ = "courses"
    __table_args__ = {
        'mariadb_ENGINE': 'mroonga',
        'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    rgno = Column(Integer,primary_key = True)
    season = Column(Text)
    ay = Column(Text)
    course_no = Column(Text)
    old_cno = Column(Text)
    lang = Column(Text)
    section = Column(Text)
    title_e = Column(Text)
    title_j = Column(Text)
    schedule = Column(Text)
    schedule_meta = Column(JSON)
    room = Column(Text)
    comment = Column(Text)
    maxnum = Column(Text)
    instructor = Column(Text)
    unit = Column(Text)
    syllabus = relationship('Syllabus', back_populates='courses')

class Syllabus(Base):
    __tablename__ ="syllabi"
    __table_args__ = {
        'mariadb_ENGINE': 'mroonga',
        'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    rgno = Column(Integer, primary_key=True)
    ay = Column(String(length=5))
    term = Column(String(length=100))
    cno = Column(String(length=100))
    title_e = Column(String(length=300))
    title_j = Column(String(length=300))
    lang = Column(String(length=300))
    instructor = Column(String(length=100))
    unit_e = Column(String(length=100))
    koma_lecture_e = Column(String(length=10))
    koma_seminar_e = Column(String(length=10))
    koma_labo_e = Column(String(length=10))
    koma_act_e = Column(String(length=10))
    koma_int_e = Column(String(length=10))
    descreption = Column(Text)
    descreption_j = Column(Text)
    goals = Column(Text)
    goals_j = Column(Text)
    content = Column(Text)
    content_j = Column(Text)
    lang_of_inst = Column(Text)
    pollicy = Column(Text)
    individual_study = Column(Text)
    ref = Column(Text)
    notes = Column(Text)
    schedule = Column(String(length=500))
    url = Column(String(length=300))
    course_rgno = Column(Integer, ForeignKey('courses.rgno'))
    courses = relationship('Course', back_populates='syllabus')

class Summary(Base):
    __tablename__="summary"
    __table_args__ = {
    'mariadb_ENGINE': 'mroonga',
    'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    rgno=sa.Column(sa.Integer,ForeignKey(Syllabus.rgno),primary_key=True)
    summary=sa.Column(sa.Text)
    summary_j=sa.Column(sa.Text)
    summary_e=sa.Column(sa.Text)
    other=sa.Column(sa.Text)

Base.metadata.create_all(engine)

#start session 
Session = sa.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

#fetch all regID from syllabus table
result = session.query(Syllabus.rgno).all()
regIdList=[]
for row in result:
    regIdList.append(row[0])


#using that data, make a loop of calling each row write errors to file.

for id in tqdm(regIdList):
    q = session.query(Summary).filter(Summary.rgno == id)
    if session.query(q.exists()).scalar() == True:
        continue
    else: 
        
        try:
            #fetch the regid entry row from syllabus table
            content = session.query(Syllabus).filter(Syllabus.rgno == id).one()
        except:
            print("error in getting course content")
        #make content query string 
        qry = """
For both Japanese and English portions in the following text, make a one paragraph summary in their respectable languages and return both summaries with the title being the language used.

Full Description / 概要
{descreption}

{descreption_j}


Learning Goals / 学修目標
{goals}

{goals_j}


Contents / 内容
{content}

{content_j}


Language of Instruction / 教授言語の詳細
{lang}
ASS

Grading Policy / 成績評価基準
{pollicy}


Notes / 注意事項
{notes}
        """.format(**content.__dict__)

        #Send to gpt3.5-turbo
        try:
            completion = client.chat.completions.create(model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "user", "content": qry}
            ],
            timeout=60)
        except Exception as e:
            print(e)
            rgno=str(content.__dict__["rgno"])
            print('passing' + rgno)
            f = open("errIDs.txt","a")
            f.write(str(e))
            f.write(str(content.__dict__["rgno"])+"\n")
            f.close()
            continue

        x = str(completion.choices[0].message.content)
        results = re.split(":*\n+(?=[\d\w])",x)
        if len(results) >5:
            rgno=str(content.__dict__["rgno"])
            print('passing' + rgno)
            f = open("errIDs.txt","a")
            f.write('too long, passing '+str(content.__dict__["rgno"])+"\n")
            f.close()
        summary_j = None
        summary_e = None
        summaries=[]
        for result in results:
            if len(result) > 30:
                summaries.append(result)
                lang = detect(result)
                print(lang)
                if lang == 'ja':
                    summary_j = result
                else:
                    summary_e = result

        summary = '\n'.join(summaries)
        print(results,end="\n\n")
        print(summary_j,end="\n\n")
        print(summary_e)
        
        session.merge(
            Summary(rgno = id, summary = summary, summary_j = summary_j, summary_e = summary_e,other= len(results))
        )