import schedule

from scraping import ScrapePrice
from db import DatabaseInsertion

def scrap_data():
    
    obj = ScrapePrice(r"app/yahoo_btc_config.json")

    price = obj.get_price()
    
    db = DatabaseInsertion()

    db.insert_data(
        element=("app, price"),
        data = ("BTC", price)
    )
    
scrap_data()