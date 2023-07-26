import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
import mysql.connector


class DatabaseInsertion:
    
    def __init__(self) -> None:
        
        load_dotenv()
        
        self.db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv(
                "MYSQL_PASSWORD"
            ),
            database=os.getenv("MYSQL_DB"),
        )
        
        self.current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.db:
            
            print("The connection is success")
        
    #------------------------------------------------------------------------#
    
    def insert_data(self, element: tuple, data: tuple):
        
        cursor = self.db.cursor()
        
        element = f"(date, {element})"
        
        tuple(["date"] + list(element))

        sql = f"""
            INSERT INTO {os.getenv("MYSQL_TABLE")} {element} 
            VALUES {self.create_insertion_element(element)};
        """
        
        data = tuple([self.current_timestamp] + list(data))
        
        print("#########################################################")
        print(sql)
        
        print("#########################################################")
        print(data)
        
        cursor.execute(sql, data)

        self.db.commit()

        print(cursor.rowcount, "record inserted.")

    
    #------------------------------------------------------------------------#
    
    @staticmethod
    def create_insertion_element(element: str):
        
        num_placeholders = len(element.split(","))
        
        # Repeat '%s' 'num_placeholders' times and join them with a space
        placeholders = ", ".join(["%s"] * num_placeholders)

        return f"({placeholders})"
    
    #------------------------------------------------------------------------#
    
#----------------------------------------------------------------------------#
        