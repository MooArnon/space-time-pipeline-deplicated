#--------#
# Import #
#----------------------------------------------------------------------------#

import os
import random
import string
from datetime import datetime, timezone, timedelta
import logging
from typing import Union

from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import pickle
import pymongo
import torch

load_dotenv()

#-------#
# Class #
#----------------------------------------------------------------------------#
# SQL Database #
#--------------#

class SQLDatabase:
    
    def __init__(
            self, 
            host: str = os.getenv("MYSQL_HOST"),
            user: str = os.getenv("MYSQL_USER"),
            password: str = os.getenv("MYSQL_PASSWORD"),
            database: str  = os.getenv("MYSQL_DB"), 
            logger: logging = None
    ) -> None:
        # Connect the SQL database
        self.connect_2_db(host, user, password, database)
        
        # Show status
        if self.db:
            logger.info("DB connected")
        
        # Time zone
        tz = timezone(timedelta(hours = 7))
        current_timestamp_raw = datetime.now(tz=tz)
        
        # current_timestamp for database insertion
        self.current_timestamp = current_timestamp_raw.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        # Get current_timestamp for partition key
        current_timestamp_key = current_timestamp_raw.strftime(
            "%Y%m%d%H%M%S"
        )
        
        # Set range of random
        # And random 10 character for partition key
        characters = string.ascii_letters + string.digits
        random_str = ''.join(
            random.choice(characters) for _ in range(10)
        )
        
        # Join date time and random string
        self.partitionkey = "_".join([current_timestamp_key, random_str])

    #-----------#
    # Insertion #
    #------------------------------------------------------------------------#
    # Main #
    #------#
    
    def insert_data(self, element: tuple, data: tuple) -> None:
        """ Insert data into the database
        
        Parameters
        ----------
        element: tuple
            Insertion element
        data: tuple
            Data
        """
        # Create insertion statement
        element = f"(insert_datetime, {element}, partitionkey)"
        tuple(["insert_datetime"] + list(element))
        
        # Query statement
        sql = f"""
            INSERT INTO {os.getenv("MYSQL_TABLE")} {element} 
            VALUES {self.create_insertion_element(element)};
        """
        
        # Create data
        data = tuple(
            [self.current_timestamp] + list(data) + [self.partitionkey]
        )
        
        # Execute query
        self.cursor.execute(sql, data)
        self.db.commit()
        
    #------------------------------------------------------------------------#
    
    def insert_prediction(self, element: tuple, data: tuple) -> None:
        """ Insert prediction into the target database
        
        Parameters
        ----------
        element: tuple
            Insertion element
        data: tuple
            Data
        """
        # Create element
        element = f"({element})"

        # Insertion query
        sql = f"""
            INSERT INTO prediction {element} 
            VALUES {self.create_insertion_element(element)};
        """
        
        # Execute the query
        self.cursor.execute(sql, data)
        self.db.commit()
        
    #---------#
    # Extract #
    #------------------------------------------------------------------------#
    
    def extract_data(
            self, 
            table_name: str, 
            number_row: int,
            condition: str
    ) -> pd.DataFrame:
        """ Extract dat from database
        
        Parameters
        ----------
        table_name: str
            The name of table
        number_row: int
            The number of row
        condition: str
            Where condition
            
        Returns
        -------
        pd.DataFrame
            The extracted data-frame
        """
        # Sample query to select data from a table
        query = f"""
        SELECT *
        FROM (
            SELECT * 
            FROM {table_name} 
            {condition}
            ORDER BY id DESC 
            LIMIT {number_row}
        ) as sub
        ORDER BY id ASC
        ; 
        """
        # Execute the query
        self.cursor.execute(query) 

        # Fetch all rows of the result
        rows = self.cursor.fetchall() 

        column_names = [i[0] for i in self.cursor.description]
        
        return pd.DataFrame(rows, columns=column_names)
    
    #------------#
    # Validation #
    #------------------------------------------------------------------------#
    # Check date #
    #------------#
    
    def is_duplicated_insert(
            self,
            table_name: str, 
            time_frame: str, 
            date_column: str,
        ) -> bool:
        """Check whether or not the recent inserted record have 
        the same present time, indicated timeframe as criterion.

        Parameters
        ----------
        table_name : str
            Name of target table
        time_frame : str
            `hourly` for layer of hour
        date_column : str
            Name of date of column
        
        Returns
        -------
        bool
            whether or not the record is the same
        """
        # Current timestamp to criteria
        criteria_current = self.convert_date_2_criteria(
            date=self.current_timestamp,
            criteria=time_frame,
        )
        
        # Last record to criteria
        last_record_date = self.extract_last_record(
            table_name=table_name,
            date_column=date_column,
        )
        criteria_last_record = self.convert_date_2_criteria(
            date=last_record_date,
            criteria=time_frame,
        )
        
        # Check if the extracted data and current remain the same
        if criteria_current == criteria_last_record:
            result = True
        else:
            result=False
        
        return result
    
    #------------------------------------------------------------------------#
    
    def extract_last_record(
        self, 
        table_name: str, 
        date_column: str,
        ) -> datetime:
        """Extract the last record from `table_name`.

        Parameters
        ----------
        table_name : str
            Name of target table

        Returns
        -------
        pd.Series
            Pandas series of last record.
        """
        query = f"""
            SELECT {date_column} 
            FROM {table_name}
            ORDER BY {date_column} DESC
        """
        self.cursor.execute(query)
        
        # [0] is extracting the first data from tuple
        # fetchone will always return tuple
        # Since the query always returned only one value
        date_recent_insert = self.cursor.fetchone()[0]
        
        return date_recent_insert
        
    
    #------------------------------------------------------------------------#
    
    @staticmethod
    def convert_date_2_criteria(date: Union[datetime, str], criteria: str) -> string:
        """Convert input date-time object the the criteria

        Parameters
        ----------
        date : datetime
            Date-object
        criteria : str
            Target criteria

        Returns
        -------
        string
            String of result
        """
        if criteria == 'hourly':
            date_format = "%Y-%m-%d %H"
        
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            
        return date.strftime(date_format)

    #--------------------#
    # Utilities function #
    #------------------------------------------------------------------------#
    
    def  close_connection(self):
        """Close the connection
        """
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
    
    #------------------------------------------------------------------------#
    
    @staticmethod
    def create_insertion_element(element: str):
        
        num_placeholders = len(element.split(","))
        
        # Repeat '%s' 'num_placeholders' times and join them with a space
        placeholders = ", ".join(["%s"] * num_placeholders)

        return f"({placeholders})"
    
    #------------------------------------------------------------------------#
    
    def connect_2_db(
            self,
            host: str,
            user: str,
            password: str, 
            database: str, 
    ) -> None:
        """Connect to the MySQL database, I use the default parameter
        as a environment variable

        Parameters
        ----------
        host : str, optional
            Host name, 
            by default os.getenv("MYSQL_HOST")
        user : str, optional
            User name, 
            by default os.getenv("MYSQL_USER")
        password : str, optional
            Password of database, 
            by default os.getenv("MYSQL_PASSWORD")
        database : str, optional
            The database name, 
            by default os.getenv("MYSQL_DB")
        """
        
        self.db = mysql.connector.connect(
            host=host, 
            user=user, 
            password=password, 
            database=database
        )
        
        self.cursor = self.db.cursor()
    
    #------------------------------------------------------------------------#
    
    def exec_sql_file(self, file_path: str) -> pd.DataFrame:
        """_summary_

        Parameters
        ----------
        path : str
            Path of .sql file

        Returns
        -------
        tuple
            result from fetching the cursor
        """
        # Read file
        with open(file_path, 'r') as file:
            query = file.read()
            data = pd.read_sql_query(query, self.db)

        return data
        
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

#-------#
# Class #
#----------------------------------------------------------------------------#
# Mongo Database #
#----------------#

class MongoDatabase:
    
    def __init__(
            self, 
            connection_string: str, 
            db_name: str, 
            collection_name: str    
    ) -> None:
        
        # Get connection_string from service from MONGO_CLIENT
        self.client = pymongo.MongoClient(connection_string)
        self.mongo_db = self.client[db_name]
        self.collection = self.mongo_db[collection_name]
        
    #------------------------------------------------------------------------#
    
    def disconnect(self):
        """Close the MOngo connection
        """
        self.client.close()
    
    #------------------------------------------------------------------------#
    
    def load_mongo_model(self, model_name: str) -> torch.nn.Module:
        """Load the machine learning model

        Parameters
        ----------
        model_name : str
            The name of model

        Returns
        -------
        torch.module
            The torch model
        """
        # Find the model
        if retrieved_model_document := self.collection.find_one(
            {"name": model_name}
        ):
            # Load model using pickle
            model = pickle.loads(
                retrieved_model_document["model"]
            )
            
        return model
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#