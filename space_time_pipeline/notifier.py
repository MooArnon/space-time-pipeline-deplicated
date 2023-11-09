#--------#
# Import #
#----------------------------------------------------------------------------#

import os

import requests
from dotenv import load_dotenv

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
                    "present_price": "<PRESENT PRICE>"
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
            'content-type':'application/x-www-form-urlencoded',
            'Authorization':'Bearer '+os.getenv("SIGNAL_NOTIFIER_TOKEN")
        }
    
    #------------------------------------------------------------------------#
    
    def sent_message(self, app_element: dict, mode: str) -> None:
        """Send message via line
        
        Parameters
        ----------
        mode: str
            if predict, generate prediction body
            if production_fail, generate fail statement
        """
        if mode == "predict":
            message = self.get_predict_body(app_element)
        
        # Sent request
        requests.post(
            self.url, 
            headers=self.headers, 
            data = {'message':message},
        )
