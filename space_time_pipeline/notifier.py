#--------#
# Import #
#----------------------------------------------------------------------------#

import os
from typing import Union

import requests
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

#----------#
# Classes #
#----------------------------------------------------------------------------#

class Notifier:
    """Base class for sending message via API
    """
    def __init__(self) -> None:
        pass
    
    #------#
    # Main #
    #------------------------------------------------------------------------#
    # Send email #
    #------------#
    
    def get_predict_body(
            self, 
            app_element: dict
    ) -> None:
        """Send email

        Parameters
        ----------
        app_element : list[dict]
            Element of app
            [
                {
                    "app": "<APP NAME>",
                    "present_price": "<PRESENT PRICE>",
                    "next_price": "<PREDICTED PRICE>"
                },
                {
                    <OTHER APP WITH THE SAME STRUCTURE>
                }
            ]
        """
        len_app = len(app_element['app']) + 1
        
        cal_element = self.calculate(
            app_element["present_price"], 
            app_element["next_price"],
        )
        
        body = f"""
        
        {app_element['app']}
        {"-" * len_app}
        
        {cal_element["signal"]} 
        
        confidence = {cal_element['confidence']}
        present_price = {cal_element['present_price']}
        next_price = {cal_element['next_price']}
        """
        
        return body
    
    #------------------------------------------------------------------------#
    @staticmethod
    def calculate(present_price: float, next_price: float) -> tuple:
        
        diff_price = (next_price - present_price)
        
        # Create signal
        if diff_price < 0:
            signal = "sell"
        elif diff_price > 0:
            signal = "buy"
        elif diff_price == 0:
            signal = "hold"
        
        # confidence
        confidence = 100 * abs(diff_price/present_price)
        
        # Wrap up element
        element = {
            "present_price": present_price,
            "next_price": next_price,
            "signal": signal,
            "confidence": round(confidence, 5)
        }
        
        return element
        
    #-----------#
    # Utilities #
    #------------------------------------------------------------------------#

    @staticmethod
    def convert_df_2_png(
        df: pd.DataFrame, 
        image_name: str,
    ) -> None:
        """Convert pandas.DataFrame to picture, exported 
        to local machine

        Parameters
        ----------
        df : pd.DataFrame
            Target data-frame
        """
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Hide the axes
        ax.axis("off")

        # Plot the table
        ax.table(
            cellText=df.values, 
            colLabels=df.columns, 
            cellLoc='center', 
            loc='center'
        )

        # Save the figure as an image
        plt.savefig(
            image_name, 
            dpi=300, 
            bbox_inches='tight', 
            pad_inches=0.05, 
            transparent=True
        )
        
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#

class LineNotifier(Notifier):
    
    def __init__(self) -> None:
        """Initialize instance

        Parameters
        ----------
        app_element : list[dict]
            Element of app
            [
                {
                    "app": "<APP NAME>",
                    "present_price": "<PRESENT PRICE>"
                    "next_price": "<PREDICTED PRICE>"
                },
                {
                    <OTHER APP WITH THE SAME STRUCTURE>
                }
            ]
        """
        self.url = 'https://notify-api.line.me/api/notify'
        self.headers = {
            #'content-type':'application/x-www-form-urlencoded',
            'Authorization':'Bearer '+os.getenv("SIGNAL_NOTIFIER_TOKEN")
        }
    
    #--------------#
    # Sent message #
    #------------------------------------------------------------------------#
    
    def sent_message(self, app_element: Union[dict, str], mode: str) -> None:
        """Send message via line
        
        Parameters
        ----------
        mode: str
            if predict, generate prediction body
            if production_fail, generate fail statement
        """
        if mode == "predict":
            message: str = self.get_predict_body(app_element)
            
        else:
            message: str = app_element
        # Sent request
        requests.post(
            self.url, 
            headers=self.headers, 
            data = {'message':message},
        )
    
    #------------#
    # Sent image #
    #------------------------------------------------------------------------#
    
    def sent_image(self, image_path: str, message: str) -> None:
        """Send file at line
        
        Parameters
        ----------
        file_path : str
            Path of txt file
        """
        files = {'imageFile': open(image_path, 'rb')}
        
        requests.post(
            self.url,
            headers=self.headers,
            data={'message': message},
            files=files
        )
    
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#
