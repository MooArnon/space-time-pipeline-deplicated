# from experiment.web_scaping import ScrapePrice
from app.scraping import ScrapePrice

sp = ScrapePrice(r"experiment\web_scaping\yahoo_btc_config.json")

price = sp.get_price()

print(price)
