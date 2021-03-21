'''Functions related to the textual UI.'''
from prettytable import from_db_cursor


def printWelcome():

    print('''
    █████████████████████████████████████████████████████████████████████████
    █▄─█▀▀▀█─▄█▄─▄▄─█▄─▄███─▄▄▄─█─▄▄─█▄─▀█▀─▄█▄─▄▄─███─▄─▄─█─▄▄─█████████████
    ██─█─█─█─███─▄█▀██─██▀█─███▀█─██─██─█▄█─███─▄█▀█████─███─██─█░░██░░██░░██
    ▀▀▄▄▄▀▄▄▄▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▀▀▀▄▄▄▀▀▄▄▄▄▀▄▄▀▀▄▄▀▀▄▄▀▀
    ''')
    print('''
            ██████╗░██╗░█████╗░████████╗████████╗░██████╗░█████╗░
            ██╔══██╗██║██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
            ██████╔╝██║███████║░░░██║░░░░░░██║░░░╚█████╗░███████║
            ██╔═══╝░██║██╔══██║░░░██║░░░░░░██║░░░░╚═══██╗██╔══██║
            ██║░░░░░██║██║░░██║░░░██║░░░░░░██║░░░██████╔╝██║░░██║
            ╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝''')


def loginInput():
    print("LOGIN")
    email = input("Please enter email: ")
    password = input("Please enter password: ")

    return email, password

def insertAndPrint(connection):
    '''Insert some inital data in the db and prints available users'''
    # Should we also insert a course maybe? Maybe the User should choose a course first.

    cursor = connection._cnx.cursor(prepared = True)

    addUser = ('''INSERT INTO User VALUES
                 (%s, %s, %s, %s, %s, %s)''')
    addFolder = ('''INSERT INTO Folder VALUES
                    (%s, %s, %s)''')
    
    userOne = (1, 'Ola', 'Nordmann', 'ola@nordmann.no', 123, 'student')
    userTwo = (2, 'Kari', 'Nordmann', 'kari@nordmann.no', 'password', 'instructor')
    folder = (1, 'Exam', None)


    try:
        cursor.execute(addUser, userOne)
        cursor.execute(addUser, userTwo)
        cursor.execute(addFolder, folder)
    except:
        # The users are already in the db.
        pass
    
    getUsers = ('SELECT * FROM User')  
    cursor.execute(getUsers) 
    userTable = from_db_cursor(cursor)
    print("The following users are available in the database:")
    print(userTable)

    connection._cnx.commit()
    cursor.close()

def printUsecases():
    print('Please try one of our extraordinary features:')
    print('''
        1. Make a post
        2. Reply to a post 
        3. Search for a keyword
        4. Compile statistics
        
        (Type 1 to write a post, 2 to reply etc. type q to quit.)
    
    ''')

def featureOne(connection):
    '''Returns the folder name chosen by the user, the text and the tag.'''

    cursor = connection._cnx.cursor(prepared = True)
    getFolderNames = ('SELECT Name FROM Folder')
    cursor.execute(getFolderNames)

    folders = []
    print("\nAvailable folders:\n ")
    for folderName in cursor:
        print(folderName[0])
        folders.append(folderName[0])

    cursor.close()

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

def featureTwo(connection):
    curs1 = connection._cnx.cursor(prepared = True)
    curs2 = connection._cnx.cursor(prepared = True)

    getPosts = ('SELECT PostID, Summary FROM Post')
    curs1.execute(getPosts)
    ids = []
    for (postID,sum) in curs1:
        ids.append(postID)
    curs1.close()

    curs2.execute(getPosts)
    print("Available posts to reply to: ")
    print(from_db_cursor(curs2))
    curs2.close()

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

