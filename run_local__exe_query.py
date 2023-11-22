from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase()

#------#
# Test #
#----------------------------------------------------------------------------#

def test_exec_query_file():
    
    report = db.exec_sql_file("report.sql")
    
    print(report.head())
    
if __name__ == "__main__":
    
    test_exec_query_file()