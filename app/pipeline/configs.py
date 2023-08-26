
#--------------------#
# Config of pipeline #
#----------------------------------------------------------------------------#

class PipelineConfig:
    
    #----------#
    # Scraping #
    #------------------------------------------------------------------------#
    # Yahoo finance #
    #---------------#
    # BTC #
    #-----#
    
    URL = "https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch&guccounter=1"
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    
    CLASS_NAME = "fin-streamer"
    CLASS = {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
    
    TAG_NAME =  "value"
    
    TRY_CONNECT = 10
    
    APP_NAME = "btc"
    
    #-------#
    # Model #
    #------------------------------------------------------------------------#
    
    MONGO_CONNECTION_STRING = "CAME FROM ENV VARIABLE"
    MONGO_DB = "spaceTimePipeline"
    MONGO_COLLECTION = "model"
    
    #------------#
    # Prediction #
    #------------------------------------------------------------------------#
    RAW_TABLE = "pipeline_db"
    