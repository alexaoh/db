"""Controller for user login."""

class User_login_ctrl:
    """Control user logins."""

    def __init__(self, connection, email, password):
        self._connection = connection
        self._email = email
        self._password = password

        # Make cursor for each object. 
        self._cursor = self._connection._cnx.cursor(prepared = True)

        #self.check_credentials()

    def check_credentials(self):
        """Checks if given password matches the password of the tuple with the given email in db."""
        select_query = "SELECT UserPassword FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()

        if not fetched_data:
            print("Your email is not registered in the database.")
            return False

        fetched_password = fetched_data[0]
        if fetched_password == self._password:
            print("Congratz, u ("+self._email+") are logged in!")
            return True
        else: 
            print("The password does not match!")
            return False

    def get_type(self):
        """Check if user is student or instructor. Return the value and save in private variable."""
        select_query = "SELECT UserType FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()[0]
        
        if not fetched_data:
            print("The email does not exist in the database.")
            return 

        self._type = fetched_data
        return self._type
        
    def get_user_id(self):
        """Find UserID of the user from the database and return it. Also save it in private variable."""
        select_query = "SELECT UserID FROM User WHERE Email = %s"
        self._cursor.execute(select_query, (self._email, )) 

        fetched_data = self._cursor.fetchone()
    
        if not fetched_data:
            print("The email does not exist in the database.")
            return 

        self._user_id = fetched_data[0]
        return self._user_id

    def insert_into_viewed_by(self, postID):
        """Insert user into ViewedBy when viewing a table."""
        # Need to check if the row exists already. 
        check_query = "SELECT UserID, PostID FROM ViewedBy WHERE (UserID = %s) AND (PostID = %s)"
        values = (self.get_user_id(), postID)
        self._cursor.execute(check_query, values)

        if not self._cursor.fetchall():
            insert_query = "INSERT INTO ViewedBy VALUES (%s, %s)"
            self._cursor.execute(insert_query, values)
            self._connection._cnx.commit() # Make sure inserted data is committed to the db.
    
    def __del__(self):
        self._cursor.close() # Each object's cursor is closed when program terminates. 
