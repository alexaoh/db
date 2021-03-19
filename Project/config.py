"""Configuration information for connecting to your database"""

import mysql.connector
from mysql.connector import errorcode


config = {
    'user': 'root',
    'password': '?????',
    'host': 'localhost',
    'database': 'DB1Project',
    'raise_on_warnings': True # Usikker på om denne trengs i tillegg til try/except nedenfor. 
}


def connect():
        """Returns a connection to the database, with credentials given by config."""
        # Open connection with error-catching. Sjekk gjennom hvordan dette fungerer til slutt. 
        #cnx = None
        try:
            cnx = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:  
                raise Exception(err) # Raised exception here to stop the program from continuing. Should probably solve differently later. 
        return cnx
