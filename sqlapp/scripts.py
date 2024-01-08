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

# Replace 'your_table_name' with the name of your table
table = metadata.tables['syllabi']

# Get a list of column names
column_names = [column.name for column in table.columns]

print(column_names)

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

