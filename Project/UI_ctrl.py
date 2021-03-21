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
        self.printWelcome()
        self.insertAndPrint()

        # Usecase 1. A student logs into the system via email and password. 
        loggedIn = False
        while not loggedIn:  
            email, password = self.loginInput()
            self.user = User_login_ctrl(self._connection, email, password)
            loggedIn = self.user.check_credentials() # Check the supplied username and password towards the User-table. 

        inp = None
        while inp != 'q':
            self.printUsecases()
            inp = input("Enter the number of the feature you would like to explore: ")
            
            if inp == '1':
                folderName, summary, text, tag = self.featureOne()
                make_post = Make_post_ctrl(self._connection, self.user, folderName)
                make_post.insert_post(summary, text, tag)

            elif inp == '2':
                reply, postID = self.featureTwo()
                make_reply = Make_reply_ctrl(self._connection, self.user, postID)
                make_reply.insert_reply(reply)

            elif inp == '3':
                keyword = self.featureThree()
                search_posts = Search_post_ctrl(self._connection)
                search_posts.total_search(keyword)

            elif inp == '4':
                statistics = Statistics_ctrl(self._connection, self.user)
                statistics.compile_stats()
            elif inp == 'q':
                pass
            else:
                print("There is no matching feature to your input.")

    def printWelcome(self):

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


    def loginInput(self):
        print("LOGIN")
        email = input("Please enter email: ")
        password = input("Please enter password: ")

        return email, password

    def insertAndPrint(self):
        """Insert some initial data in the db and print available users"""
        # Should we also insert a course maybe? Maybe the User should choose a course first.

        addUser = ("""INSERT INTO User VALUES
                    (%s, %s, %s, %s, %s, %s)""")
        addFolder = ("""INSERT INTO Folder VALUES
                        (%s, %s, %s)""")
        
        userOne = (1, 'Ola', 'Nordmann', 'ola@nordmann.no', 123, 'student')
        userTwo = (2, 'Kari', 'Nordmann', 'kari@nordmann.no', 'password', 'instructor')
        folder = (1, 'Exam', None)
        # Dette user-insert kan heller puttes i txt-filen tenker jeg.

        try:
            # Sjekk at disse tingene faktisk committes til databasen ;)) (når de utføres sekvensielt slik)
            # Jeg tror egentlig at commit() (slik som nedenfor) må kalles etter hver execute().
            # Se artikkel jeg sendte på messenger for dette også (at man kan kjøre en rollback() dersom ikke hele transaksjonen, dvs noen av disse executene ikke er successfull.)
            self._cursor.execute(addUser, userOne)
            self._cursor.execute(addUser, userTwo)
            self._cursor.execute(addFolder, folder)
        except:
            # The users are already in the db. 
            # Her kan man bruke rollback slik jeg snakker om ift artikkelen, nice!
            # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
            pass
        
        getUsers = ("SELECT * FROM User")  
        self._cursor.execute(getUsers) 
        userTable = from_db_cursor(self._cursor)
        print("The following users are available in the database:")
        print(userTable)

        self._connection._cnx.commit() # Sjekk dette ift det jeg kommenterte lenger oppe ;)

    def printUsecases(self):
        print("Please try one of our extraordinary features:")
        print("""
            1. Make a post
            2. Reply to a post 
            3. Search for a keyword
            4. Compile statistics
            
            (Type 1 to write a post, 2 to reply etc. type q to quit.)
        
        """)

    def featureOne(self):
        """Return the folder name chosen by the user, the text and the tag."""        
        getFolderNames = ("SELECT Name FROM Folder")
        self._cursor.execute(getFolderNames)

        folders = []
        print("\nAvailable folders:\n ")
        for folderName in self._cursor:
            print(folderName[0])
            folders.append(folderName[0])

        chosenFolder = False
        while not chosenFolder:
            inp = input("\nWrite the name of the folder you want to make a post in: ")
            if inp not in folders:
                print("No such folder exists.")
            else:
                chosenFolder = True
        
        summary = input("Write a summary of your post: ")
        text = input("Write your text: ")
        tag = input("Write a tag for your post: ")
        return inp, summary, text, tag

    def featureTwo(self):
        """"Returns the reply-text and post-id of which the user replies to."""
        getPosts = ("SELECT PostID, Summary FROM Post")
        self._cursor.execute(getPosts)
        ids = []
        for (postID,sum) in self._cursor.fetchall(): # Virker som at dette fungerer! Da kan de to cursorne ovenfor fjernes ;) 
            ids.append(postID)

        self._cursor.execute(getPosts)
        print("\nAvailable posts to reply to: ")
        print(from_db_cursor(self._cursor))

        chosenPost = False
        postID = None
        while not chosenPost:
            postID = input("Write the ID of the post you want to reply to: ")
            if int(postID) not in ids:
                print("No post matches the given ID.")
            else:
                chosenPost = True

        text = input("Write your reply: ")

        return text, int(postID)
    
    def featureThree(self):
        """Returns the inputted keyword to search for."""
        keyword = input("Write your search keyword: ")
        return keyword

    def __del__(self):
        self._cursor.close() # Each object's cursor is closed when program terminates.   
