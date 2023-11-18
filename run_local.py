from space_time_pipeline import SQLDatabase
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging

db = SQLDatabase(logger=logger)

element=('app, price'),
data = ("HOTFIX", 0.0001)

db.insert_data(
    element=element,
    data=data
)

