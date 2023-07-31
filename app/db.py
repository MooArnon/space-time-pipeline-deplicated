import os
import random
import string
from datetime import datetime

from dotenv import load_dotenv
import mysql.connector
import pandas as pd


class DatabaseInsertion:
    
    def __init__(self) -> None:
        
        self.connect_2_db()
        
        current_timestamp_raw = datetime.now()
        
        self.current_timestamp = current_timestamp_raw.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        
        current_timestamp_key = current_timestamp_raw.strftime(
            "%Y%m%d%H%M%S"
        )
        
        characters = string.ascii_letters + string.digits
        random_str = ''.join(
            random.choice(characters) for _ in range(10)
        )
        
        self.partitionkey = "_".join([current_timestamp_key, random_str])
        
        if self.db:
            
            print("The connection is success")
    
    #-----------#
    # Insertion #
    #------------------------------------------------------------------------#
    # Main #
    #------#
    
    def insert_data(self, element: tuple, data: tuple):
        
        cursor = self.db.cursor()
        
        element = f"(date, {element}, partitionkey)"
        
        tuple(["date"] + list(element))
        
        sql = f"""
            INSERT INTO {os.getenv("MYSQL_TABLE")} {element} 
            VALUES {self.create_insertion_element(element)};
        """
        
        data = tuple(
            [self.current_timestamp] + list(data) + [self.partitionkey]
        )
        
        print("raw data \n", data)
        
        cursor.execute(sql, data)

        self.db.commit()

        print(cursor.rowcount, "record inserted. \n")
        
        if cursor:
            cursor.close()
        if self.db:
            self.db.close()

    #------------------------------------------------------------------------#
    
    def insert_prediction(self, element: tuple, data: tuple):
        
        try: 
            cursor = self.db.cursor()
            
        except:
            self.connect_2_db()
            cursor = self.db.cursor()
        
        cursor = self.db.cursor()
        
        element = f"({element})"

        sql = f"""
            INSERT INTO prediction {element} 
            VALUES {self.create_insertion_element(element)};
        """

        print("prediction \n", data)
        
        print(sql)
        
        cursor.execute(sql, data)

        self.db.commit()

        print(cursor.rowcount, "record inserted. \n")
        
        if cursor:
            cursor.close()
        if self.db:
            self.db.close()
            
    #------------------------------------------------------------------------#
    # Function in use #
    #-----------------#
    
    @staticmethod
    def create_insertion_element(element: str):
        
        num_placeholders = len(element.split(","))
        
        # Repeat '%s' 'num_placeholders' times and join them with a space
        placeholders = ", ".join(["%s"] * num_placeholders)

        return f"({placeholders})"
    
    #------------------------------------------------------------------------#
    
    def connect_2_db(self) -> None:
        
        load_dotenv()
        
        self.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )
        
    #---------#
    # Extract #
    #------------------------------------------------------------------------#
    
    def extract_data(self, table_name: str, number_row: int):
        
        try:
            
            cursor = self.db.cursor()

            # Sample query to select data from a table
            query = f"""
                SELECT * 
                FROM {table_name} 
                ORDER BY id DESC 
                LIMIT {number_row}; 
            """

            # Execute the query
            cursor.execute(query) 

            # Fetch all rows of the result
            rows = cursor.fetchall() 
            
            column_names = [i[0] for i in cursor.description]
            df = pd.DataFrame(rows, columns=column_names)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if self.db:
                self.db.close()
                
            return df
    
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#
