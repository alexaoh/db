"""Controller to make (instructor) reply directly to post in the forum."""

class Make_reply_ctrl:
    """Control making a new reply to an existing post."""

    def __init__(self, connection, author, post_id):
        self._connection = connection
        self._author = author
        self._author_id = author.get_user_id() 
        self._author_type = author.get_type()
        self._post_id = post_id

        # Make cursor for each object. 
        self._cursor = self._connection._cnx.cursor(prepared = True)

    def insert_reply(self, text):
        """Insert reply into database"""
        self._text = text

        reply_insertion = "INSERT INTO ReplyPost(Text, UserID, PostID) VALUES (%s, %s, %s)"

        reply_values = (self._text, self._author_id, self._post_id)

        self._cursor.execute(reply_insertion, reply_values)
        self.output_user_type_and_insert_color_code() 
        self._connection._cnx.commit() # Make sure inserted data is committed to the db.

        print("Your reply was inserted!")

        # Keep statistics. 
        self._author.insert_into_viewed_by(self._post_id) # Insert (UserID, PostID) into ViewedBy.

    def output_user_type_and_insert_color_code(self):
        """Customize output based on author type. Insert correct ColorCode into database."""
        if self._author_type == "instructor":
            print("The instructor ("+self._author._email+") answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("yellow", self._post_id))
            self._connection._cnx.commit() # Make sure update is committed to the db.
        elif (self._author_type == "student"):
            print("The student ("+self._author._email+") answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("green", self._post_id))
            self._connection._cnx.commit() # Make sure update is committed to the db.
        else:
            raise Exception("Something went wrong... Neither a student nor an instructor answered.")

    def __del__(self):
        self._cursor.close() # Each object's cursor is closed when program terminates. 
