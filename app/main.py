#--------#
# Import #
#----------------------------------------------------------------------------#

import os
import schedule
import time

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.pipeline import flow

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#----------#
# Variable #
#----------------------------------------------------------------------------#

data_pipeline = flow

schedule.every().hour.at(":00").do(data_pipeline)


# Create a FastAPI instance
app = FastAPI()

# Add a global variable to keep track of whether the loop is running 
# or not
loop_running = False

app.mount(
    "/static", 
    StaticFiles(directory=os.path.join("app","static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join("app", "templates"))

#------#
# Root #
#----------------------------------------------------------------------------#

# Show the status of machine 
@app.get("/", response_class=HTMLResponse)
def status_page(request: Request):
    return templates.TemplateResponse(
        "status.html", {"request": request, "loop_running": loop_running}
    )
    
#----------#
# Pipeline #
#----------------------------------------------------------------------------#

def start_loop():
    global loop_running
    loop_running = True
    while True:
        # schedule.run_pending()
        time.sleep(1)

#----------------------------------------------------------------------------#

@app.post("/start-loop/")
def start_loop_endpoint():
    if loop_running:
        raise HTTPException(
            status_code=400, 
            detail="Loop is already running."
        )
    # Start the loop in a new thread to avoid blocking the API
    import threading
    threading.Thread(target=start_loop, daemon=True).start()
    return {"message": "Loop started successfully."}

#----------------------------------------------------------------------------#

# Endpoint to get the status of loop_running
@app.get("/loop-status/")
def get_loop_status():
    global loop_running
    return JSONResponse(content={"loop_running": loop_running})
