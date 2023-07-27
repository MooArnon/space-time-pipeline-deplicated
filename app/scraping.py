import requests
import json
import os

from bs4 import BeautifulSoup

class ScrapePrice:
    
    def __init__(
            self, 
            config_path: str = os.path.join(
                "app", "yahoo_btc_config.json"
            )
    ) -> None:
        
        self.config = self.read_config(config_path)
    
    #------------------------------------------------------------------------#
    
    def get_price(self):
        
        doc = self.get_page(self.config["url"], self.config["header"])

        tag = doc.find_all(
            self.config["price_element"]["java_class"]["class_name"], 
            self.config["price_element"]["java_class"]["class"]
        )[0]
        
        price = tag[self.config["price_element"]["tag_name"]]

        return float(price)
    
    #------------------------------------------------------------------------#

    def get_page(self, url: str, header: dict):  
        
        req = requests.get(url, headers=header)
        
        if not req.ok:
            
            raise Exception(f"Failed to connect to {self.url}")

        page_content = req.text
        
        return BeautifulSoup(page_content, 'html.parser')

    #------------------------------------------------------------------------#
    
    @staticmethod
    def read_config(path: str) -> dict:
        
        with open(path) as file:
            
            config = json.load(file)
            
        return config
    
#----------------------------------------------------------------------------#   
