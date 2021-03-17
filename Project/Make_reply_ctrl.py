"""Controller to make (instructor) reply directly to post in the forum."""

from DB_connector import DB_connector

class Make_reply_ctrl(DB_connector):
    """Controls making a new reply to an existing post."""

    def __init__(self, author, post_id):
        DB_connector.__init__(self)
        self._author_id = author.get_user_id() 
        self._author_type = author.get_type()
        self._post_id = post_id

    def insert_reply(self, text):
        """Insert reply into database"""
        self._text = text

        self._cursor = self._cnx.cursor(prepared=True)

        reply_insertion = "INSERT INTO ReplyPost(Text, UserID, PostID) VALUES (%s, %s, %s)"

        reply_values = (self._text, self._author_id, self._post_id)

        self._cursor.execute(reply_insertion, reply_values)
        self.output_user_type_and_insert_color_code() 
        self._cnx.commit() # Make sure inserted data is committed to the db.
        self._cursor.close() # Close the cursor when done.

        print("Your reply was inserted!")

    def output_user_type_and_insert_color_code(self):
        """Customize output based on author type. Insert correct ColorCode into database."""
        if self._author_type == "instructor":
            print("instructor answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("yellow", self._post_id))
        elif (self._author_type == "student"):
            print("student answered!")
            update_colorcode = "UPDATE Post SET ColorCode = %s WHERE PostID = %s"
            self._cursor.execute(update_colorcode, ("green", self._post_id))
        else:
            raise Exception("something went wrong... Neither student nor instructor answer")
