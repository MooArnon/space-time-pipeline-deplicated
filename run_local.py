import torch
import os

from app.db import Database
from app.predict import Prediction

from app.validate import validate_db

db = Database()

"""
model = load_model("nn")

print(type(model))

model = Prediction(model, "nn")

df = db.extract_data("pipeline_db", model.get_input_shape)

# Price lst
price_lst = df["price"].tolist()
price_lst.reverse()

result = model.predict(price_lst, "nn")

print(result)
"""
"""
model = torch.load(
    os.path.join(
        "etc", "secrets", "model", "NN_btc-hourly__20230729_180557.pth"
    )
)

insert_model(model, "nn")
"""

df = db.extract_data("pipeline_db", 5)

print(df.head(5))
