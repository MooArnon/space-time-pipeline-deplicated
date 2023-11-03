#--------#
# Import #
#----------------------------------------------------------------------------#

from space_time_pipeline import BeautifulSoupEngine

#-------#
# Class #
#----------------------------------------------------------------------------#

class TestEngine:
    
    bs_engine = BeautifulSoupEngine()
    
    def test_scraped_type(self):
        """ The type of scraped must be float type.
        """
        
        price = self.bs_engine.scrape()
        
        assert type(price) == float  # noqa: E721
    
    #------------------------------------------------------------------------#
    
    def test_scraped_not_0(self):
        """Scraped must not be 0.
        """
        price = self.bs_engine.scrape()
        
        print(price)
        
        assert price != 0 
        assert price != 0.0
        assert price != 0.00 # noqa: E721
        
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#
