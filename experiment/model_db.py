import os
import pickle

import torch
import pymongo
from bson.binary import Binary


model = torch.load(
    os.path.join("etc", "secrets", "model", "NN_btc-hourly__20230729_180557.pth")
)

# Save the model to MongoDB
client = pymongo.MongoClient(
    "mongodb+srv://oomarnon2542:Oomkingu5@spacetime.pnkqta5.mongodb.net/"
)
db = client["spaceTimePipeline"]
collection = db["model"]

#----------------------------------------------------------------------------#

def insert_model(model, model_name):
    # Serialize the model's parameters using pickle and convert to BSON binary
    model_parameters = pickle.dumps(model.state_dict())
    binary_model_parameters = Binary(model_parameters)

    # Create a document and insert it into the collection
    model_document = {
        "name": model_name, 
        "model_parameters": binary_model_parameters
    }
    collection.insert_one(model_document)

#----------------------------------------------------------------------------#

def load_model(model_name):
    
    if retrieved_model_document := collection.find_one(
        {"name": model_name}
    ):
        model_parameters = pickle.loads(
            retrieved_model_document["model_parameters"]
        )
        model.load_state_dict(model_parameters)

    return model

if __name__ == "__main__":
    
    model = load_model("nn")
    
    print(model)
    