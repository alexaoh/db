"""Main application program."""

from User_login_ctrl import User_login_ctrl
from Make_post_ctrl import Make_post_ctrl

if __name__ == "__main__":

    # Perhaps make some sort of menu or complete textual UI later?
    # All the arguments from the use cases should be given via a UI. 

    # Usecase 1. A student logs into the system via email and password. 
    user = User_login_ctrl("ola@nordmann.com", "heisann sveisann")

    user.connect() # Connect to the database. Should perhaps be done automatically when the object is made?
    user.check_credentials() # Check the supplied username and password towards the User-table. 
    #user.close_connection() # Close connection. Should this be done automatically inside the connector-class perhaps? How?
    
    # Seems like the connection should not be closed before moving on. Not sure how this should be treated!? Need to read in docs!

    # Usecase 2. A student makes a post belonging to the folder "Exam", tagged with "Question". Input is text, "Exam", "Question".

    # Should probably check if the user is logged in before the post can be made also somehow?

    make_post = Make_post_ctrl(user, "Exam")
    make_post.connect()
    make_post.insert_post("This is a student's post", "Hello! I have a question regarding Exam H2022. How is task 3 calculated?", 
                            "Question")     
    make_post.close_connection()

    # Usecase 3. An instructor replies to a post belonging to the folder "Exam". The input to this is the id of the post replied to. For instance, the post in usecase 2
    instructor = User_login_ctrl("kari@nordmann.no", "hade på badet")
    instructor.connect()
    instructor.check_credentials()

    make_reply = Make_reply_ctrl(instructor, 1)
    make_reply.connect()
    make_reply.insert_reply("The answer to your question will always be 42")
    make_reply.close_connection()