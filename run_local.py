from web_scaping import ScrapePrice

obj = ScrapePrice(r"web_scaping/yahoo_btc_config.json")

price = obj.get_price()

print(type(price))
