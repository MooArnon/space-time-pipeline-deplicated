#--------#
# Import #
#----------------------------------------------------------------------------#

from dotenv import load_dotenv
import pandas as pd

import os
from email.message import EmailMessage
import ssl
import smtplib


#----------#
# Variable #
#----------------------------------------------------------------------------#

sender_mail = "space.time.pipeline@gmail.com"
SENDER_EMAIL_PASSWORD = "gtqduqktqpmhqqzp"

subject = "Space Time prediction"


#----------#
# Classes #
#----------------------------------------------------------------------------#

class EmailManagement:
    
    def __init__(self) -> None:
        pass
    
    #------#
    # Main #
    #------------------------------------------------------------------------#
    # Send email #
    #------------#
    
    def send_email(
            self, 
            sender_mail: str,
            user_df: pd.DataFrame, 
            app_element: list[dict]
    ):
        
        for idx, row in user_df.iterrows():
            
            self.send_email_element(
                sender_mail=sender_mail,
                receiver_email=row["email"],
                app_element=app_element
            )
    
    #------------------------------------------------------------------------#
    
    def send_email_element(
            self, 
            sender_mail: str, 
            receiver_email: str, 
            app_element: list[dict]
    ):
        load_dotenv()
        
        em = EmailMessage()
        em["From"] = sender_mail
        em["To"] = receiver_email
        em["Subject"] = "Space Time Prediction"
        
        body = self.get_body(app_element)

        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)  as smtp:
            
            smtp.login(sender_mail, os.getenv("SENDER_EMAIL_PASSWORD"))
            
            smtp.sendmail(
                msg=em.as_string(), 
                from_addr=sender_mail, 
                to_addrs=receiver_email
            )
                
    #------#
    # Body #
    #------------------------------------------------------------------------#
    
    def get_body(
            self, 
            element: list[dict]
    ) -> str:
        """" Create body

        Parameters
        ----------
        element : dict :
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

        Returns
        -------
        str
            _description_
        """
        body = """
        The predictions of space time are below
        
        """
        
        for app_element in element:
            
            body += self.get_element(
                app = app_element["app"],
                present_price = app_element["present_price"],
                next_price = app_element["next_price"],
            )
            
        return body
    
    #------------------------------------------------------------------------#
    
    def get_element(
            self, 
            app: str, 
            present_price: float,
            next_price: float, 
    ) -> str:

        return f"""
        {app}:
        {"="*(len(app)+1)}
        PRESENT price is : {present_price}.
        The price for the NEXT HOUR is: {next_price}.
        Signal is: {100*(next_price - present_price)/present_price} %.
        
    """
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
