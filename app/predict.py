import torch
import pandas as pd

class Prediction:
    
    def __init__(self, path_model: str, type: str) -> None:
        
        if type == 'nn':
            
            self.model = torch.load(path_model)
            
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
        