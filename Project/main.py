"""Main application program."""


from DB_connector import *
from User_login_ctrl import User_login_ctrl
from Make_post_ctrl import Make_post_ctrl
from Make_reply_ctrl import Make_reply_ctrl
from Search_post_ctrl import Search_post_ctrl
from Statistics_ctrl import Statistics_ctrl



if __name__ == "__main__":

    # Perhaps make some sort of menu or complete textual UI later?
    # All the arguments from the use cases should be given via a UI. 

    globalCnx = connect()
    
    # Usecase 1. A student logs into the system via email and password. 
    user = User_login_ctrl(globalCnx, "ola@nordmann.com", "heisann sveisann")
    user.check_credentials() # Check the supplied username and password towards the User-table. 
    

    # Usecase 2. A student makes a post belonging to the folder "Exam", tagged with "Question". Input is text, "Exam", "Question".

    # Should probably check if the user is logged in before the post can be made also somehow?
    if(globalCnx): print("Connection is open")
    make_post = Make_post_ctrl(globalCnx, user, "Exam")
    make_post.insert_post("This is a student's post", "Hello! I have a question regarding Exam H2022. How is task 3 calculated?", "Question")     


    # Usecase 3. An instructor replies to a post belonging to the folder "Exam". The input to this is the id of the post replied to. For instance, the post in usecase 2
    instructor = User_login_ctrl(globalCnx, "kari@nordmann.no", "hade på badet")
    instructor.check_credentials()

    make_reply = Make_reply_ctrl(globalCnx, instructor, 1)
    make_reply.insert_reply("The answer to your question will always be 42")
    
    # Usecase 4. A student searches for posts with a specific keyword "WAL".

    student = User_login_ctrl(globalCnx, "alex@vektor.no", "123456")
    student.check_credentials()

    search_posts = Search_post_ctrl(globalCnx, student)
    search_posts.total_search("WAL")

    # Usecase 5. Compile statistics. 
    statistics = Statistics_ctrl(globalCnx, instructor)
    statistics.compile_stats()


    globalCnx.close()