#--------#
# Import #
#----------------------------------------------------------------------------#

import os
from datetime import datetime, timezone, timedelta

from app.pipeline import (
    BeautifulSoupEngine,
    SQLDatabase,
    DeepPrediction,
)
from app.pipeline.email_sending import EmailManagement
from app.pipeline.configs import PipelineConfig

#----------------------------------------------------------------------------#


def flow():
    """The flow controlling function.
    """
    #------------------#
    # Initialize class #
    #------------------------------------------------------------------------#
    
    # Scraper
    scraper = BeautifulSoupEngine()
    
    # SQL database
    sql_db = SQLDatabase(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DB"), 
    )
    
    # Prediction
    prediction_nn = DeepPrediction("nn")
    
    mail = EmailManagement()
    
    
    #------#
    # Flow #
    #------------------------------------------------------------------------#
    # Insert price data #
    #-------------------#
    
    # Scrape price
    price = scraper.scrape()
    
    # Insert scraped
    sql_db.insert_data(
        element=("app, price"),
        data = (PipelineConfig.APP_NAME, price)
    )
    
    
    #------------------------------------------------------------------------#
    # Insert prediction #
    #-------------------#
    
    # Extract data
    df_extracted = sql_db.extract_data(
        table_name = PipelineConfig.RAW_TABLE,
        number_row = prediction_nn.get_input_shape,
        condition = None
    )
    
    # Prediction
    predict, model = prediction_nn.predict_deep(df_extracted["price"].tolist())

    # Partitionkey
    partitionkey_lst = df_extracted["partitionkey"].tolist()
    partitionkey = partitionkey_lst[-1]
    
    # App
    app = df_extracted["app"].to_list()[-1]
    
    # All data
    data = tuple([partitionkey] + [app] + ["nn"] + [predict])
    
    # Insert prediction
    sql_db.insert_prediction(
        element = ('partitionkey, app, model, prediction'),
        data = data
    )
    
    #------------------------------------------------------------------------#
    # Send email #
    #------------#
    
    # Create app element
    app_element = {
        "app": app,
        "present_price": price,
        "next_price": predict,
    }
    
    # Get all users
    user_df = sql_db.extract_data(
        table_name="user",
        number_row=10,
        condition="WHERE privilege NOT LIKE '%admin%'"
    )
    
    # Send email
    mail.send_email(
        sender_mail="space.time.pipeline@gmail.com",
        user_df=user_df,
        app_element=[app_element]
    )
    
    tz = timezone(timedelta(hours = 7))
    print(f'Finish loop {datetime.now(tz).isoformat(sep = " ")}')
    
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#
