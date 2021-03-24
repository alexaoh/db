"""Class for connecting to MySQL database."""

import mysql.connector
from mysql.connector import errorcode

class DB_connector:

    def __init__(self):
        self._config = {
            # Match 'user' with your username and 'password' with your password. 
            'user': '',
            'password': '',
            'database': 'Piattsa',
            'host': '127.0.0.1',
            'raise_on_warnings': True 
        }
        self.connect() # Make a connection to the database. 

    def connect(self):
        """Connect to database, with credentials given in config."""
        
        try:
            self._cnx = mysql.connector.connect(**self._config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_connection(self):
        """Close connection."""
        self._cnx.close()

    def __del__(self):
        self.close_connection()
        