"""Userlogin."""

from DBConnector import DBConnector

class Userlogin(DBConnector):

    def __init__(self, email, password):
        DBConnector.__init__(self)
        self.email = email
        self.password = password

    def check_credentials(self):
        self.cursor = self.cnx.cursor()
        select_query = "SELECT UserPassword FROM User WHERE Email = %s"
        self.cursor.execute(select_query, (self.email, )) # Dette kommaet måtte med, men litt usikker på hvorfor. Sjekk dette senere!

        fetched_data = self.cursor.fetchall()
        if not fetched_data:
            print("Your email is not registered in the database.")
            return 

        fetched_password = fetched_data[0][0]
        if fetched_password == self.password:
            print("Congratz, u r logged in!")
            return 
    