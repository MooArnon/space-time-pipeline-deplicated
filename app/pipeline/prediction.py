#--------#
# Import #
#----------------------------------------------------------------------------#

import os
from typing import Union
from abc import abstractmethod

import torch
from space_time_modeling.modeling.resources.nn import NNModel 

from app.pipeline.db import MongoDatabase



#---------#
# Classes #
#----------------------------------------------------------------------------#

class BasePrediction:
    
    @abstractmethod
    def predict():
        """ Be use the create prediction 
        by indicated model model
        """
        
        raise NotImplementedError("Child class must implement predict")
    
    #------------------------------------------------------------------------#
    
    def load_model(self, model_architecture: str):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        if model_architecture == "deep":
            
            mongo_db = MongoDatabase(
                connection_string=os.getenv("MONGO_CLIENT"),
                db_name="spaceTimePipeline",
                collection_name="model"
            )

            model = mongo_db.load_mongo_model("nn")
            
        mongo_db.disconnect()
        
        return model

#----------------------------------------------------------------------------#
# Deep #
#------#

class DeepPrediction(BasePrediction):
    
    def __init__(
            self, 
            type_model: str,  
            model: Union[str, NNModel] = "load_mongo",     
    ) -> None:
        
        # Load model
        # If model is nn
        if type_model == 'nn':
            
            # Model path
            if model == "load_mongo":
                self.model = self.load_model("deep")
            
            # Model it self
            elif isinstance(model, NNModel):
                self.model = model

    #------#
    # Main #
    #------------------------------------------------------------------------#
    
    def predict(self, price_lst: list, type: str):
        """ Run prediction

        Parameters
        ----------
        price_lst : list
            list of price
        type : str
            Type of model

        Returns
        -------
        _type_
            _description_
        """
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
    
    def predict_deep(self, price_lst: list) -> tuple[float, str]:
        
        model_type = "nn"
        
        feature = torch.tensor([price_lst[-self.get_input_shape:]])
        
        return self.model(feature).item(), model_type
        
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#  
        