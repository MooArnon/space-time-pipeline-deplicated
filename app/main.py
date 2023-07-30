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

from app.scraping import ScrapePrice
from app.db import DatabaseInsertion


#----------#
# Variable #
#----------------------------------------------------------------------------#

# Create a FastAPI instance
app = FastAPI()

# Add a global variable to keep track of whether the loop is running or not
loop_running = False

# NN model
model_nn = torch.load(
    os.path.join(
        "etc", "secrets", "model", "NN_btc-hourly__20230729_180557.pth"
    )
)
input_shape_nn = model_nn.state_dict()['linears.0.weight'].shape[1]

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

#-----------------#
# Function in use #
#----------------------------------------------------------------------------#
# Scrape data #
#-------------#

def scrap_data():
    obj = ScrapePrice(os.path.join("app", "yahoo_btc_config.json"))

    price = obj.get_price()
    
    if not price:
        
        time.sleep(60)
        
        price = obj.get_price()
    
    db = DatabaseInsertion()

    db.insert_data(
        element=("app, price"),
        data = ("btc", price)
    )
    
    write_prediction()
#----------------------------------------------------------------------------#
# Prediction #
#------------#

def write_prediction() -> None:
    
    db = DatabaseInsertion()
    
    df = db.extract_data("pipeline_db", input_shape_nn)
    
    print(df.head())
    
    # Price lst
    price_lst = df["price"].tolist()
    price_lst.reverse()
    
    partitionkey_lst = df["partitionkey"].tolist()
    partitionkey_lst.reverse()
    
    predict, model_type = predict_nn(price_lst)
    
    partitionkey = partitionkey_lst[-1]
    
    app = df["app"].to_list()[-1]
    
    data = tuple([partitionkey] + [app] +[model_type] + [predict])
    
    db.insert_prediction(
        element = ('partitionkey, app, model, prediction'),
        data = data
    )

#----------------------------------------------------------------------------#

def predict_nn(price_lst: pd.Series) -> float:
    
    global model_nn, input_shape_nn
    
    model_type = "nn"

    feature = torch.tensor([price_lst[-input_shape_nn:]])
    
    return model_nn(feature).item(), model_type

#----------#
# Schedule #
#----------------------------------------------------------------------------#

schedule.every().hour.at(":00").do(scrap_data)
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
    write_prediction()