import schedule

from web_scaping import ScrapePrice
from db import DatabaseInsertion

def scrap_data():
    
    obj = ScrapePrice(r"web_scaping/yahoo_btc_config.json")

    price = obj.get_price()
    
    db = DatabaseInsertion()

    db.insert_data(
        element=("app, price"),
        data = ("test_02", price)
    )
    
schedule.every().minute.at(":17").do(scrap_data)