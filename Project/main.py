"""Main application program."""

from User_login_ctrl import User_login_ctrl

if __name__ == "__main__":

    # Perhaps make some sort of menu or complete textual UI later?

    # Usecase 1
    userlogin = User_login_ctrl("ola@nordmann.com", "heisann sveisann")

    userlogin.connect() # Connect to the database. Should perhaps be done automatically when the object is made?
    userlogin.check_credentials() # Check the supplied username and password towards the User-table. 
    userlogin.close_connection() # Close connection. Should this be done automatically inside the connector-class perhaps? How?
    
    # Usecase 2

