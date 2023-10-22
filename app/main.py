#--------#
# Import #
#----------------------------------------------------------------------------#

import os
import schedule
import time
import threading
import logging

from dotenv import load_dotenv

from fastapi import FastAPI
from app.pipeline import flow
from fastapi.responses import HTMLResponse

#----------#
# Variable #
#----------------------------------------------------------------------------#

logging.basicConfig(  
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("space-time--pipeline")

load_dotenv()

# Create a FastAPI instance
app = FastAPI()

#----------#
# Pipeline #
#----------------------------------------------------------------------------#

def pipeline_with_logger(logger):
    try:
        flow(logger)  # Call data_pipeline with the logger
    except Exception as e:
        logger.error(f"Error in data_pipeline: {str(e)}")

#----------------------------------------------------------------------------#

def assign_schedule(run_mode: str):

    if run_mode == "prod":
        schedule.every().hour.at(":00").do(pipeline_with_logger, logger)
        logger.info("Using prod mode")
        
    elif run_mode == "dev":
        schedule.every().minute.at(":00").do(pipeline_with_logger, logger)
        logger.info("Using dev mode")

    else:
        raise ValueError(f"THERE ARE NO {run_mode} in program")

#----------------------------------------------------------------------------#

def start_loop():
    
    while True:
        schedule.run_pending()
        time.sleep(1)

#----------------------------------------------------------------------------#

@app.post("/start-loop/")
def start_loop_endpoint():
    
    assign_schedule(os.getenv("RUN_MODE"))
    
    threading.Thread(target=start_loop, daemon=True).start()
    
    return {"message": "Loop started successfully."}

#------#
# Root #
#----------------------------------------------------------------------------#

# Show the status of machine 
@app.get("/", response_class=HTMLResponse)
def status_page():
    return {"API": "WORKED"}

if __name__ == "__main__":
    
    print("Wowza")
