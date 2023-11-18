from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase(logger=logger)

result = db.exec_sql_file(file_path="select.sql")

print(result)
