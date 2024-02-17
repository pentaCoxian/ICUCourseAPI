from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, JSON
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .database import Base

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
    rgno=Column(sa.Integer,ForeignKey('courses.rgno'),primary_key=True)
    summary=Column(sa.Text)
    summary_j=Column(sa.Text)
    summary_e=Column(sa.Text)
    other=Column(sa.Text)

# SELECT syllabi.cno, syllabi.term, syllabi.title_j, syllabi.title_j AS title_j__1, syllabi.rgno, syllabi.lang 
# FROM syllabi INNER JOIN courses ON courses.rgno = summary.rgno 
# WHERE syllabi.term IN ('Spring Term', 'Autumn Term', 'Winter Term') AND MATCH (syllabi.title_j, syllabi.title_e, syllabi.instructor, syllabi.descreption, syllabi.descreption_j, syllabi.goals, syllabi.goals_j, syllabi.content, syllabi.content_j, syllabi.lang_of_inst, syllabi.pollicy, syllabi.individual_study, syllabi.ref, syllabi.notes, syllabi.schedule) AGAINST ('+test' IN BOOLEAN MODE) ORDER BY MATCH (syllabi.title_j, syllabi.title_e, syllabi.instructor, syllabi.descreption, syllabi.descreption_j, syllabi.goals, syllabi.goals_j, syllabi.content, syllabi.content_j, syllabi.lang_of_inst, syllabi.pollicy, syllabi.individual_study, syllabi.ref, syllabi.notes, syllabi.schedule) AGAINST ('+test') DESC]
# [parameters: (, , , '+test', '+test')
