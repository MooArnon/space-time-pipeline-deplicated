#--------#
# Import #
#----------------------------------------------------------------------------#

import os
import time
from datetime import datetime, timezone, timedelta

# Import FastAPI
from fastapi import FastAPI, HTTPException
import schedule
import pymongo
from dotenv import load_dotenv

from app.scraping import ScrapePrice
from app.db import Database
from app.predict import Prediction
from app.email_sending import EmailManagement

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
mail = EmailManagement()

#-------#
# Model #
#----------------------------------------------------------------------------#
# Mongo parameter #
#-----------------#

# Save the model to MongoDB
client = pymongo.MongoClient(
    os.getenv("MONGO_CLIENT")
)

# Get model's collection
mongo_db = client["spaceTimePipeline"]
collection = mongo_db["model"]

#----------------------------------------------------------------------------#
# NN model #
#----------#

print("Loading nn model")
model_nn = db.load_mongo_model("nn")
model_nn = Prediction(model_nn, "nn")
print(f"Loading completed {model_nn}")

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
# Root #
#------#
# Endpoint to check the loop status
@app.get("/")
def root():
    return {"Start-loop": "Go to /start-loop/ to run",
            "Loop is running": loop_running
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

#-----------------#
# Function in use #
#----------------------------------------------------------------------------#
# Main #
#------#

def main():
    
    #-------------#
    # Scrape data #
    #------------------------------------------------------------------------#
    print("\nStart scrape data")
    app_name, present_price = scrap_data("btc")

    #----------------#
    # Run prediction #
    #------------------------------------------------------------------------#
    # run prediction
    print("Start predict")
    predict = write_prediction()

    #------------#
    # Send email #
    #------------------------------------------------------------------------#
    # Create app_element body
    # Update app_element body
    #! Temporary for the 
    app_element = {
        "app": app_name,
        "present_price": present_price,
        "next_price": predict,
    }
    
    # Get all users
    user_df = db.extract_data(
        table_name="user",
        number_row=10,
        condition="WHERE privilege NOT LIKE '%admin%'"
    )

    # Send email
    mail.send_email(
        sender_mail="space.time.pipeline@gmail.com",
        user_df=user_df,
        app_element=[app_element]
    )

    tz = timezone(timedelta(hours = 7))

    print(f'Finish loop {datetime.now(tz).isoformat(sep = " ")}')

#----------------------------------------------------------------------------#
# Scrape data #
#-------------#

def scrap_data(app_name: str) -> float:
    
    db = Database()
    
    obj = ScrapePrice(os.path.join("app", "yahoo_btc_config.json"))

    price = obj.get_price()
    
    if not price:
        
        time.sleep(60)
        
        price = obj.get_price()
    
    db.insert_data(
        element=("app, price"),
        data = (app_name, price)
    )
    
    return app_name, price
    
#----------------------------------------------------------------------------#
# Prediction #
#------------#

def write_prediction() -> None:
    
    global model_nn
    
    db = Database()
    
    # Extract data from data base
    df = db.extract_data(
        "pipeline_db", 
        model_nn.get_input_shape,
        condition=None
    )

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
    
    return predict

#----------#
# Schedule #
#----------------------------------------------------------------------------#

schedule.every().hour.at(":00").do(main)
# schedule.every(1).minutes.do(main)
now = datetime.now()

#--------#
# Freeze #
#----------------------------------------------------------------------------#

# Your existing main running block remains unchanged
if __name__ == "__main__":
    print(f"Running engine at {now.strftime('%H:%M:%S')}")
    
    main()