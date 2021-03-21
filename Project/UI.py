'''Functions related to the textual UI.'''
from logging import NullHandler
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
    cursor = connection._cnx.cursor(prepared = True)

    addUser = ('''INSERT INTO User VALUES
                 (%s, %s, %s, %s, %s, %s)''')
    addFolder = ('''INSERT INTO Folder VALUES
                    (%s, %s, %s)''')
    
    userOne = (1, 'Ola', 'Nordmann', 'ola@nordmann.no', 123, 'student')
    userTwo = (2, 'Kari', 'Nordmann', 'kari@nordmann.no', 'password', 'instructor')

    folder = (1, 'Exam', None)
    cursor.execute(addFolder, folder)

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

