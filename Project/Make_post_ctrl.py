"""Controller to make a new post in the forum."""

from DB_connector import DB_connector

class Make_post_ctrl(DB_connector):
    """Controls making of new posts."""

    def __init__(self, author, folder_name):
        DB_connector.__init__(self)
        author.find_user_id() # Finds user ID and stores it in author.user_id. Perhaps more logical to just return it via a getter?
        self._author_id = author._user_id
        self._folder_name = folder_name

    def insert_post(self, summary, main_text, tag):
        """Insert post into database."""
        self._summary = summary
        self._text = main_text
        self._tag = tag
    
        self._cursor = self._cnx.cursor(prepared = True)

        insert_into_post = """INSERT INTO Post(Text, Summary, ColorCode, Tag, FolderID, UserID) VALUES 
                                    (%s, %s, %s, %s, %s, %s)"""

        values = (self._text, self._summary, "red", self._tag, self.get_folder_id(), self._author_id)

        self._cursor.execute(insert_into_post, values)
        self._cnx.commit() # Make sure inserted data is committed to the db.
        self._cursor.close() # Close the cursor when done. 

        print("Your post was inserted!")

    def get_folder_id(self):
        """Find FolderID that belongs to the folder-name given in constructor."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT FolderID FROM Folder WHERE Name = %s"
        self._cursor.execute(select_query, (self._folder_name, )) 

        fetched_data = self._cursor.fetchone()
    
        if not fetched_data:
            print("A folder with the name "+self._folder_name+" does not exist in the database.")
            return 

        self._folder_id = fetched_data[0]
        return self._folder_id
