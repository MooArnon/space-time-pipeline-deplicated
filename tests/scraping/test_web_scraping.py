from web_scaping import ScrapePrice

def test_type_scraping():

    obj = ScrapePrice(r"web_scaping/yahoo_btc_config.json")

    price = obj.get_price()
    
    assert isinstance(price, float)
