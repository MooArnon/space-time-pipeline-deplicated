import os

import mysql.connector
from dotenv import load_dotenv

def check_db_connection():
    try:
        load_dotenv()
            
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        )

        print("The connection is success")

    except mysql.connector.Error as e:
        print("Error connecting to MySQL: ", e)

if __name__ == "__main__":
    
    check_db_connection()