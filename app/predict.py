from typing import Union

import torch
import pandas as pd
from space_time_modeling.modeling.resources.nn import NNModel 

class Prediction:
    
    def __init__(self, model: Union[str, NNModel], type_model: str) -> None:
        
        if type_model == 'nn':
            
            if isinstance(model, str):
                
                self.model = torch.load(model)
            
            elif isinstance(model, NNModel):
                
                self.model = model

    #------#
    # Main #
    #------------------------------------------------------------------------#
    
    def predict(self, price_lst: list, type: str):
        
        if type == "nn":
            
            prediction = self.predict_deep(price_lst)
            
        return prediction
    
    #----------#
    # NN model #
    #------------------------------------------------------------------------#
    
    @property
    def get_input_shape(self):
        return self.model.state_dict()['linears.0.weight'].shape[1]
    
    #------------------------------------------------------------------------#
    
    def predict_deep(self, price_lst: list):
        
        model_type = "nn"
        
        feature = torch.tensor([price_lst[-self.get_input_shape:]])
        
        return self.model(feature).item(), model_type
        
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#  
        