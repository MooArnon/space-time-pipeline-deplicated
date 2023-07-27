#--------#
# Import #
#----------------------------------------------------------------------------#

import os

# Import FastAPI
from fastapi import FastAPI, HTTPException

# Import other modules as needed
import time
from datetime import datetime
import schedule
from app.scraping import ScrapePrice
from app.db import DatabaseInsertion

#----------#
# Variable #
#----------------------------------------------------------------------------#

# Create a FastAPI instance
app = FastAPI()

# Add a global variable to keep track of whether the loop is running or not
loop_running = False

#------------#
# API things #
#----------------------------------------------------------------------------#
# Start & Stop #
#--------------#

# Function to start the loop
def start_loop():
    global loop_running
    loop_running = True
    while True:
        schedule.run_pending()
        time.sleep(1)

#----------------------------------------------------------------------------#

# Function to stop the loop
def stop_loop():
    global loop_running
    loop_running = False

#----------------------------------------------------------------------------#
# Endpoint #
#----------#

# New endpoint to start the loop
@app.post("/start-loop/")
def start_loop_endpoint():
    if not loop_running:
        # Start the loop in a new thread to avoid blocking the API
        import threading
        threading.Thread(target=start_loop, daemon=True).start()
        return {"message": "Loop started successfully."}
    else:
        raise HTTPException(status_code=400, detail="Loop is already running.")

#----------------------------------------------------------------------------#

# Endpoint to check the loop status
@app.get("/loop-status/")
def loop_status():
    return {"loop_running": loop_running}

# Endpoint to check the loop status
@app.get("/")
def root():
    return {"Start-loop": "Go to /start-loop/ to run",
            "Check-status": "Loop-status"
            }

#----------------------------------------------------------------------------#

def scrap_data():
    obj = ScrapePrice(os.path.join("app", "yahoo_btc_config.json"))

    price = obj.get_price()
    
    if not price:
        
        time.sleep(60)
        
        price = obj.get_price()
    
    db = DatabaseInsertion()

    db.insert_data(
        element=("app, price"),
        data = ("test_04", price)
    )

#----------------------------------------------------------------------------#

schedule.every().hour.at(":00").do(scrap_data)

now = datetime.now()

# Your existing main running block remains unchanged
if __name__ == "__main__":
    print(f"Running engine at {now.strftime('%H:%M:%S')}")
    while True:
        schedule.run_pending()
        time.sleep(1)
