from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase(logger=logger)

#------#
# Test #
#----------------------------------------------------------------------------#

def test_connection():
    
    #------------------------------------------------------------------------#
    # Insert raw data #
    #-----------------#
    element=('app, price'),
    data = ("HOTFIX", 0.0001)

    db.insert_data(
        element=element,
        data=data
    )
    print("\nINSERT SUCCESSFULLY\n")

    #------------------------------------------------------------------------#
    # Extract data #
    #--------------#

    data = db.extract_data(
        table_name = "pipeline_db",
        number_row = 3,
    )

    print(data)
    print("\nEXTRACT SUCCESSFULLY\n")

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    test_connection()
    
#----------------------------------------------------------------------------#
