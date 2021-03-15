"""Main application program."""

from Userlogin import Userlogin

if __name__ == "__main__":
    userlogin = Userlogin("ola@nordmann.com", "heisann sveisann")

    userlogin.connect() # Connect to the database. Should perhaps be done automatically when the object is made?
    userlogin.check_credentials() # Check the supplied username and password towards the User-table. 
    