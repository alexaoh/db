"""Class for connecting to MySQL database."""

import mysql.connector
from mysql.connector import errorcode

class DB_connector():

    def __init__(self):
        self.config = {
            'user': 'dbprojectuser',
            'password': 'admin',
            'host': '127.0.0.1',
            'database': 'DB1Project',
            'raise_on_warnings': True # Usikker på om denne trengs i tillegg til try/except nedenfor. 
        }

    def connect(self):
        """Connect to database, with credentials given in config."""

        # Open connection with error-catching. Sjekk gjennom hvordan dette fungerer til slutt. 
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_connection(self):
        """Close connection."""
        self.cnx.close()
