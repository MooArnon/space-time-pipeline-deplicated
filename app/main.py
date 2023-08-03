#--------#
# Import #
#----------------------------------------------------------------------------#

import os
import time
from datetime import datetime

# Import FastAPI
from fastapi import FastAPI, HTTPException
import schedule
import torch
import pandas as pd
import pymongo
from dotenv import load_dotenv

from app.scraping import ScrapePrice
from app.db import Database
from app.predict import Prediction

#----------#
# Variable #
#----------------------------------------------------------------------------#
# API #
#-----#

load_dotenv()

print("Connect to: ", os.getenv("MYSQL_HOST"),)
print("At database name: ", os.getenv("MYSQL_DB"))

# Create a FastAPI instance
app = FastAPI()

# Add a global variable to keep track of whether the loop is running or not
loop_running = False

#----------------------------------------------------------------------------#
# Classes indication #
#--------------------#

db = Database()

#----------------------------------------------------------------------------#
# Model #
#-----------------#
# Mongo parameter #
#-----------------#

# Save the model to MongoDB
client = pymongo.MongoClient(
    os.getenv("MONGO_CLIENT")
)

mongo_db = client["spaceTimePipeline"]
collection = mongo_db["model"]

#----------------------------------------------------------------------------#
# NN model #
#----------#

model_nn = db.load_mongo_model("nn")

model_nn = Prediction(model_nn, "nn")

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
#----------------#
# Root end point #
#----------------#
# Endpoint to check the loop status
@app.get("/")
def root():
    return {"Start-loop": "Go to /start-loop/ to run",
            "Check-status": "loop-status"
            }

#----------------------------------------------------------------------------#
# Loop things # 
#-------------#

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

#-----------------#
# Function in use #
#-----------------#
# Main #
#------#

def main():
    
    scrap_data()
    
    write_prediction()

#----------------------------------------------------------------------------#
# Scrape data #
#-------------#

def scrap_data():
    
    global db
    
    obj = ScrapePrice(os.path.join("app", "yahoo_btc_config.json"))

    price = obj.get_price()
    
    if not price:
        
        time.sleep(60)
        
        price = obj.get_price()
    
    db.insert_data(
        element=("app, price"),
        data = ("btc", price)
    )
    
#----------------------------------------------------------------------------#
# Prediction #
#------------#

def write_prediction() -> None:
    
    global model_nn, db
    
    # Extract data from data base
    df = db.extract_data("pipeline_db", model_nn.get_input_shape)

    # Price lst
    price_lst = df["price"].tolist()
    price_lst.reverse()
    
    # Partitionkey
    partitionkey_lst = df["partitionkey"].tolist()
    partitionkey_lst.reverse()
    partitionkey = partitionkey_lst[-1]
    
    # App
    app = df["app"].to_list()[-1]
    
    # Predict
    predict, model_type = model_nn.predict(price_lst, "nn")
    
    # Convert data to tuple
    data = tuple([partitionkey] + [app] +[model_type] + [predict])
    
    # Insert prediction to database
    db.insert_prediction(
        element = ('partitionkey, app, model, prediction'),
        data = data
    )

#----------#
# Schedule #
#----------------------------------------------------------------------------#

schedule.every().hour.at(":00").do(main)
now = datetime.now()

#--------#
# Freeze #
#----------------------------------------------------------------------------#

# Your existing main running block remains unchanged
if __name__ == "__main__":
    print(f"Running engine at {now.strftime('%H:%M:%S')}")
    
    """ SCRAPE AND INSERT
    while True:
        schedule.run_pending()
        time.sleep(1)
    """
    # write_prediction()