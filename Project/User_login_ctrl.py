"""Userlogin."""

from DB_connector import DB_connector

class User_login_ctrl(DB_connector):
    """Controls user logins."""
    # Perhaps we need to differentiate between instructors and students at some point?  
    # Will leave this be for now. 

    def __init__(self, email, password):
        DB_connector.__init__(self)
        self.email = email
        self.password = password

    def check_credentials(self):
        """Checks if given password matches the password of the tuple with the given email in db."""
        self.cursor = self.cnx.cursor(prepared = True)
        select_query = "SELECT UserPassword FROM User WHERE Email = %s"
        self.cursor.execute(select_query, (self.email, )) # Dette kommaet måtte med, men litt usikker på hvorfor. Sjekk dette senere!

        fetched_data = self.cursor.fetchone()
        self.cursor.close() # Close the curso when done. 

        if not fetched_data:
            print("Your email is not registered in the database.")
            return 

        fetched_password = fetched_data[0]
        if fetched_password == self.password:
            print("Congratz, u r logged in!")
            return 
        else: 
            print("The password does not match!")
    