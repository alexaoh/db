"""Main application program."""

from UI import *
from DB_connector import DB_connector
from User_login_ctrl import User_login_ctrl
from Make_post_ctrl import Make_post_ctrl
from Make_reply_ctrl import Make_reply_ctrl
from Search_post_ctrl import Search_post_ctrl
from Statistics_ctrl import Statistics_ctrl

if __name__ == "__main__":
    printWelcome()

    # Make connection-object first.
    connection = DB_connector()
    insertAndPrint(connection)
    
    # Usecase 1. A student logs into the system via email and password. 
    loggedIn = False
    while not loggedIn:  
        email, password = loginInput()
        user = User_login_ctrl(connection, email, password) #"ola@nordmann.com", "heisann sveisann"
        loggedIn = user.check_credentials() # Check the supplied username and password towards the User-table. 

    # Usecase 2. A student makes a post belonging to the folder "Exam", tagged with "Question". Input is text, "Exam", "Question".

    make_post = Make_post_ctrl(connection, user, "Exam") # Use already logged in user to make post. 
    make_post.insert_post("This is a student's post", "Hello! I have a question regarding Exam H2022. How is task 3 calculated?", "Question")     

    # Usecase 3. An instructor replies to a post belonging to the folder "Exam". The input to this is the id of the post replied to. For instance, the post in usecase 2. 
    instructor = User_login_ctrl(connection, "kari@nordmann.no", "hade på badet")

    make_reply = Make_reply_ctrl(connection, instructor, 1)
    make_reply.insert_reply("The answer to your question will always be 42")
    
    # Usecase 4. A student searches for posts with a specific keyword "WAL".
    student = User_login_ctrl(connection, "alex@vektor.no", "123456")

    search_posts = Search_post_ctrl(connection, student)
    search_posts.total_search("WAL")
  
    # Usecase 5. Compile statistics. 
    statistics = Statistics_ctrl(connection, instructor)
    statistics.compile_stats()
