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
    room: str
    comment: str
    maxnum: str
    instructor: str
    unit: str
    # ids: int

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    class Config:
        orm_mode: True