"""Controller for the UI."""
from prettytable import from_db_cursor
from User_login_ctrl import User_login_ctrl
from Make_post_ctrl import Make_post_ctrl
from Make_reply_ctrl import Make_reply_ctrl
from Search_post_ctrl import Search_post_ctrl
from Statistics_ctrl import Statistics_ctrl

class UI_ctrl:

    def __init__(self, connection):
        self._connection = connection
        self._cursor = self._connection._cnx.cursor(prepared = True)
        self.user = None

    def main(self):
        self.print_welcome()
        self.print_available_users()

        # Usecase 1. A student logs into the system via email and password. 
        logged_in = False
        while not logged_in:  
            email, password = self.login_input()
            self.user = User_login_ctrl(self._connection, email, password)
            logged_in = self.user.check_credentials() # Check the supplied username and password towards the User-table. 

        inp = None
        while inp != 'q':
            self.print_usecases()
            inp = input("Enter the number of the feature you would like to explore: ")
            
            if inp == '1':
                folder_name, summary, text, tag = self.feature_one()
                make_post = Make_post_ctrl(self._connection, self.user, folder_name)
                make_post.insert_post(summary, text, tag)

            elif inp == '2':
                reply, postID = self.feature_two()
                make_reply = Make_reply_ctrl(self._connection, self.user, postID)
                make_reply.insert_reply(reply)

            elif inp == '3':
                keyword = self.feature_three()
                search_posts = Search_post_ctrl(self._connection)
                search_posts.total_search(keyword)

            elif inp == '4':
                statistics = Statistics_ctrl(self._connection, self.user)
                statistics.compile_stats()
            elif inp == 'q':
                pass
            else:
                print("There is no matching feature to your input.")

    def print_welcome(self):

        print("""
        █████████████████████████████████████████████████████████████████████████
        █▄─█▀▀▀█─▄█▄─▄▄─█▄─▄███─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─███─▄─▄─█─▄▄─█████████████
        ██─█─█─█─███─▄█▀██─██▀█─███▀█─██─██─█▄█─███─▄█▀█████─███─██─█░░██░░██░░██
        ▀▀▄▄▄▀▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▄▄▀▀▄▄▀▀▄▄▀▀
        """)
        print("""
                ██████╗░██╗░█████╗░████████╗████████╗░██████╗░█████╗░
                ██╔══██╗██║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
                ██████╔╝██║███████║░░░██║░░░░░░██║░░░╚█████╗░███████║
                ██╔═══╝░██║██╔══██║░░░██║░░░░░░██║░░░░╚═══██╗██╔══██║
                ██║░░░░░██║██║░░██║░░░██║░░░░░░██║░░░██████╔╝██║░░██║
                ╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝""")


    def login_input(self):
        print("LOGIN")
        email = input("Please enter email: ")
        password = input("Please enter password: ")

        return email, password

    def print_available_users(self):
        """Print available users"""
        # Perhaps the User should choose a course first. Se på dette! 
        # Course can ev legges inn via exampleData.txt.
        
        getUsers = ("SELECT * FROM User")  
        self._cursor.execute(getUsers) 
        userTable = from_db_cursor(self._cursor)
        print("The following users are available in the database:")
        print(userTable)

    def print_usecases(self):
        """Print use case menu to choose from in this light version of Piatssa."""
        print("Please try one of our extraordinary features:")
        print("""
            1. Make a post
            2. Reply to a post 
            3. Search for a keyword
            4. Compile statistics
            
            (Type 1 to write a post, 2 to reply etc. type q to quit.)
        
        """)

    def feature_one(self):
        """Return the folder name chosen by the user, the text and the tag."""        
        get_folder_names = ("SELECT Name FROM Folder")
        self._cursor.execute(get_folder_names)

        folders = []
        print("\nAvailable folders:\n ")
        for folder_name in self._cursor.fetchall():
            print(folder_name[0])
            folders.append(folder_name[0])

        chosen_folder = False
        while not chosen_folder:
            inp = input("\nWrite the name of the folder you want to make a post in: ")
            if inp not in folders:
                print("No such folder exists.")
            else:
                chosen_folder = True
        
        summary = input("Write a summary of your post: ")
        text = input("Write your text: ")
        tag = input("Write a tag for your post: ")
        return inp, summary, text, tag

    def feature_two(self):
        """"Return the reply-text and post-id of which the user replies to."""
        get_posts = ("SELECT P.PostID, P.Summary, F.Name as Folder FROM Post as P INNER JOIN Folder as F USING (FolderID)")
        self._cursor.execute(get_posts)
        ids = []
        for (postID,sum,name) in self._cursor.fetchall():
            ids.append(postID)

        self._cursor.execute(get_posts)
        print("\nAvailable posts to reply to: ")
        print(from_db_cursor(self._cursor))

        chosen_post = False
        postID = None
        while not chosen_post:
            postID = input("Write the ID of the post you want to reply to: ")
            try:
                postID = int(postID)
                if postID not in ids:
                    print("No post matches the given ID.")
                else:
                    chosen_post = True
            except ValueError:
                print("Please input an integer data type.")

        text = input("Write your reply: ")

        return text, postID
    
    def feature_three(self):
        """Take input and return the keyword to search for."""
        keyword = input("Write your search keyword: ")
        return keyword

    def __del__(self):
        self._cursor.close() # Each object's cursor is closed when program terminates.   
