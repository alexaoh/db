"""Controller to make (instructor) reply directly to post in the forum."""

from DB_connector import DB_connector

class Make_reply_ctrl(DB_connector):
    """Controls making a new reply to an existing post."""

    def __init__(self, author, post_id):
        DB_connector.__init__(self)
        author.find_user_id() # Finds user id
        self._author_id = author._user_id
        self._post_id = post_id

    def insert_reply(self, text):
        """Insert reply into database"""
        self._text = text

        self._cursor = self._cnx.cursor(prepared=True)

        reply_insertion = "INSERT INTO Replypost(Text, UserID, PostID) VALUES (%s, %s, %s)"

        reply_values = (self._text, self._author_id, self._post_id)

        self._cursor.execute(reply_insertion, reply_values)
        self.get_user_type()
        self._cnx.commit() # Make sure inserted data is committed to the db.
        self._cursor.close() # Close the cursor when done.

        print("Your reply was inserted!")

    def get_user_type(self):
        select_type = "SELECT UserType FROM User WHERE UserID = %s"
        self._cursor.execute(select_type, (self._author_id, ))

        fetched_data = self._cursor.fetchone()

        if not fetched_data:
            print("User does not exist. Error")
            return
        else:
            print(fetched_data)

        self._author_type = fetched_data[0]
        if self._author_type == 'instructor':
            print("instructor answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("yellow", self._post_id))
        elif (self._author_type == "student"):
            print("student answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("green", self._post_id))
        else:
            print("something went wrong... Neither student nor instructor answer")