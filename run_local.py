from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase(logger=logger)

print(
        db.is_duplicated_insert(
            "pipeline_db",
            time_frame='hourly',
            date_column='insert_datetime',
    )
)
