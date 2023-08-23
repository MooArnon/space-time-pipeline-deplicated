#--------#
# Import #
#----------------------------------------------------------------------------#

import requests
import time

from bs4 import BeautifulSoup

from app.pipeline.config import PipelineConfig


#---------#
# Classes #
#----------------------------------------------------------------------------#

class BaseScape:
    

#----------------------------------------------------------------------------#

class ScrapePrice:
    
    def __init__(self) -> None:
        pass
    #------------------------------------------------------------------------#
    
    def scrape(self) -> float:
        """ Scrape price

        Returns
        -------
        float
            Scraped price as float
        """
        # Get page data
        doc = self.get_page(PipelineConfig.URL, PipelineConfig.USER_AGENT)

        # Find the price on page
        tag = doc.find_all(
            PipelineConfig.CLASS_NAME, 
            PipelineConfig.CLASS
        )[0]
        
        # Get price from tag name
        price = tag[PipelineConfig.TAG_NAME]

        return float(price)
    
    #------------------------------------------------------------------------#

    def get_page(self, url: str, header: dict) -> BeautifulSoup:  
        """ Get the page data

        Parameters
        ----------
        url : str
            target url
        header : dict
            target header

        Returns
        -------
        BeautifulSoup
            Soup type of page

        Raises
        ------
        Exception
            Raise if failed to connect
        """
        # 
        for _ in PipelineConfig.TRY_CONNECT:
            
            # Get requirement
            req = requests.get(url, headers=header)
            
            # IF requirement is OK
            # Break loop
            if req.ok:
                
                break
            
            time.sleep(15)
        
        # If requirement is not found
        # Raise exception
        if not req.ok:
            raise Exception(f"Failed to connect to {self.url}")
        
        return BeautifulSoup(req.text, 'html.parser')

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#   
