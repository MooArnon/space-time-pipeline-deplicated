from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase()

#------#
# Test #
#----------------------------------------------------------------------------#

def test_connection():
    
    #------------------------------------------------------------------------#
    # Insert raw data #
    #-----------------#
    # element=('app, price'),
    # data = ("HOTFIX", 0.0001)
    
    # Check if data insert or not
    inserted: bool = db.is_duplicated_insert(
        table_name="pipeline_db",
        time_frame="hourly",
        date_column="insert_datetime"
    )
    
    # Insert data, if there are not recent record inserted at database
    if inserted is False:
        db.insert_data(
            element=('app', 'price'),
            data = ("test", 0.9918)
        )
    
    # Insert nothing, if the pipeline was retire, and last insert
    # was completed
    elif inserted is True:
        logger.info("INSERT NOTHING | RETIRED TASK")
        
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
