import os

from app.scraping import ScrapePrice

def test_type_scraping():

    obj = ScrapePrice(os.path.join("app", "yahoo_btc_config.json"))

    price = obj.get_price()
    
    assert isinstance(price, float)
