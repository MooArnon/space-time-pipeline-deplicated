# from experiment.web_scaping import ScrapePrice
from app.db import DatabaseInsertion
from app.main import write_prediction
"""
db = DatabaseInsertion()

db.insert_data(
        element=("app, price"),
        data = ("btc", 9999999)
    )
"""

write_prediction()