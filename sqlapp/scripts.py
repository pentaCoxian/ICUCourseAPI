from sqlalchemy import create_engine, MetaData, DDL, event
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.environ['MARIADB_ADDRESS']

# Create an SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define a metadata object and bind it to the engine
metadata = MetaData()
metadata.reflect(bind=engine)

table = metadata.tables["syllabi"]
# Iterate over and drop all indexes except the primary key
for index in list(table.indexes):
    print(f"Dropping index: {index.name}")
    index.drop(bind=engine)

"""
SELECT syllabi.title_e, syllabi.title_j, courses.instructor
FROM syllabi
INNER JOIN courses ON courses.rgno = syllabi.course_rgno 
WHERE MATCH(syllabi.title_e,syllabi.title_j) AGAINST('+asia' IN BOOLEAN MODE);"""

''' 
Alter table syllabi ADD FULLTEXT INDEX test_idx(title_j,title_e,instructor,descreption,descreption_j,goals,goals_j,content,content_j,lang_of_inst,pollicy,individual_study,ref,notes,schedule) COMMENT 'tokenizer "TokenMecab"'
'''



# # Replace 'your_table_name' with the name of your table
# table = metadata.tables['syllabi']

# # Get a list of column names
# column_names = [column.name for column in table.columns]

# print(column_names)

# def create_fulltext_index(table, index_name, columns):
#     columns_str = ', '.join(columns)
#     sql_statement = f"CREATE FULLTEXT INDEX {index_name} ON {table} ({columns_str});"
#     return DDL(sql_statement)

# def makeFullTextIndex(db: Session, tablename: str, indexname: str, field: str):
#     sql = """ALTER TABLE """ + tablename + """ ADD FULLTEXT INDEX IF NOT EXISTS """ + indexname +  """(""" + field + """) COMMENT 'tokenizer "TokenMecab"';"""
#     return db.execute(text(sql))

# columns_to_index = ['title_e', 'title_j']

# # Creating the full-text index
# fulltext_index = create_fulltext_index('courses', 'idx_fulltext_title', columns_to_index)

# # Attaching the event to create the index after the table is created
# event.listen(Syllabus.__table__, 'after_create', fulltext_index)


# class Course(Base):
#     __tablename__ = "courses"
#     __table_args__ = {
#         'mariadb_ENGINE': 'mroonga',
#         'mariadb_DEFAULT_CHARSET': 'utf8mb4'
#     }
#     rgno = Column(Integer,primary_key = True)
#     season = Column(Text)
#     title_e = Column(Text)
#     title_j = Column(Text)
#     schedule = Column(Text)
#     schedule_meta = Column(JSON)
#     room = Column(Text)
#     comment = Column(Text)
#     maxnum = Column(Text)
#     instructor = Column(Text)
#     unit = Column(Text)
#     syllabus = relationship('Syllabus', back_populates='courses')

# class Syllabus(Base):
#     __tablename__ ="syllabi"
#     __table_args__ = {
#         'mariadb_ENGINE': 'mroonga',
#         'mariadb_DEFAULT_CHARSET': 'utf8mb4'
#     }
#     rgno = Column(Integer, primary_key=True)
#     ay = Column(String(length=5))
#     term = Column(String(length=100))
#     title_e = Column(String(length=300))
#     title_j = Column(String(length=300))
#     notes = Column(Text)
#     schedule = Column(String(length=500))
#     url = Column(String(length=300))
#     course_rgno = Column(Integer, ForeignKey('courses.rgno'))
#     courses = relationship('Course', back_populates='syllabus')
