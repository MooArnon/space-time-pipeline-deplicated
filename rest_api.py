#--------#
# Import #
#----------------------------------------------------------------------------#
from fastapi import FastAPI
from pydantic import BaseModel

#-----------#
# Variables #
#----------------------------------------------------------------------------#

app = FastAPI()

class TestItem(BaseModel):
    
    text: str

#-----#
# App #
#----------------------------------------------------------------------------#

@app.get("/")
def read_root(): 
    return {"Hello": "World"}

#----------------------------------------------------------------------------#

@app.post("/text")
def render_text(item: TestItem):
    
    output = f"{item.text}"
    
    return {
        "Render": output
    }

#----------------------------------------------------------------------------#
