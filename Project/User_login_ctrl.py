"""Controller for user login."""

from DB_connector import DB_connector

class User_login_ctrl(DB_connector):
    """Controls user logins."""

    def __init__(self, email, password):
        DB_connector.__init__(self)
        self._email = email
        self._password = password

    def check_credentials(self):
        """Checks if given password matches the password of the tuple with the given email in db."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT UserPassword FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()
        #self._cursor.close() # Close the cursor when done. 

        if not fetched_data:
            print("Your email is not registered in the database.")
            return 

        fetched_password = fetched_data[0]
        if fetched_password == self._password:
            print("Congratz, u r logged in!")
            return 
        else: 
            print("The password does not match!")

    def get_type(self):
        """Check if user is student or instructor. Return the value and save in private variable."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT UserType FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()[0]
        #self._cursor.close() # Close the cursor when done. 
        
        if not fetched_data:
            print("The email does not exist in the database.")
            return 

        self._type = fetched_data
        return self._type
        
    def get_user_id(self):
        """Find UserID of the user from the database and return it. Also save it in private variable."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT UserID FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()
        #self._cursor.close() # Close the cursor when done. 
    
        if not fetched_data:
            print("The email does not exist in the database.")
            return 

        self._user_id = fetched_data[0]
        return self._user_id

    def insert_into_viewed_by(self, postID):
        """Insert user into ViewedBy when viewing a table."""
        self._cursor = self._cnx.cursor(prepared=True)
        insert_query = "INSERT INTO ViewedBy VALUES (%s, %s)"
        values = (self.get_user_id(), postID)
        self._cursor.execute(insert_query, values)
        #self._cursor.close()
        self._cnx.commit() # Make sure inserted data is committed to the db.
