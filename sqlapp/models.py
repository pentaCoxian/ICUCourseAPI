from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

load_dotenv()

engine = create_engine(os.environ['MARIADB_ADDRESS'],echo=True)
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"
    rgno = Column(Text,primary_key = True)
    season = Column(Text)
    ay = Column(Text)
    course_no = Column(Text)
    old_cno = Column(Text)
    lang = Column(Text)
    section = Column(Text)
    title_e = Column(Text)
    title_j = Column(Text)
    schedule = Column(Text)
    room = Column(Text)
    comment = Column(Text)
    maxnum = Column(Text)
    instructor = Column(Text)
    unit = Column(Text)
