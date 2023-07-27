#--------#
# Import #
#----------------------------------------------------------------------------#
import time
from datetime import datetime

import schedule

from scraping import ScrapePrice
from db import DatabaseInsertion

#----------#
# function #
#----------------------------------------------------------------------------#

def scrap_data():
    
    obj = ScrapePrice(r"app/yahoo_btc_config.json")

    price = obj.get_price()
    
    if not price:
        
        time.sleep(60)
        
        price = obj.get_price()
    
    db = DatabaseInsertion()

    db.insert_data(
        element=("app, price"),
        data = ("test_04", price)
    )

#-------------------#
# Schedule variable #
#----------------------------------------------------------------------------#

schedule.every().hour.at(":00").do(scrap_data)

now = datetime.now()

#-------------#
# Main running #
#----------------------------------------------------------------------------#

if __name__ == "__main__":
    
    print(f"Running engine at {now.strftime('%H:%M:%S')}")
    
    while True:
        schedule.run_pending()
        time.sleep(1)