from pydantic import BaseModel

class CourseBase(BaseModel):
    rgno: str
    season: str
    ay: str
    course_no: str
    old_cno: str
    lang: str
    section: str
    title_e: str
    title_j: str
    schedule: str
    schedule_meta: list
    room: str
    comment: str
    maxnum: str
    instructor: str
    unit: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    class Config:
        orm_mode: True
    
class SyllabusBase(BaseModel):
    rgno: int
    ay:str
    term:str
    cno:str
    title_e:str
    title_j:str
    lang:str
    instructor:str
    unit_e:str
    koma_lecture_e:str
    koma_seminar_e:str
    koma_labo_e:str
    koma_act_e:str
    koma_int_e:str
    descreption: str
    descreption_j: str
    goals: str
    goals_j: str
    content: str
    content_j: str
    lang_of_inst: str
    pollicy: str
    individual_study: str
    ref: str
    notes: str
    schedule: str
    url: str
    course_rgno: int

class SyllabusCreate(SyllabusBase):
    pass

class Syllabus(SyllabusBase):
    class Config:
        orm_mode: True
