"""Controller to make a new post in the forum."""

class Make_post_ctrl:
    """Control making of new posts."""

    def __init__(self, connection, author, folder_name):
        self._connection = connection
        self._author = author
        self._author_id = author.get_user_id() 
        self._folder_name = folder_name

        # Make cursor for each object. 
        self._cursor = self._connection._cnx.cursor(prepared = True)

    def insert_post(self, summary, main_text, tag):
        """Insert post into database."""
        self._summary = summary
        self._text = main_text
        self._tag = tag
        
        insert_into_post = """INSERT INTO Post(Text, Summary, ColorCode, Tag, FolderID, UserID) VALUES 
                                    (%s, %s, %s, %s, %s, %s)"""
                                    
        values = (self._text, self._summary, "red", self._tag, self.get_folder_id(), self._author_id)

        self._cursor.execute(insert_into_post, values)
        self._connection._cnx.commit() # Make sure inserted data is committed to the db.
        
        print("Your post was inserted!")

        # Keep statistics. 
        postID = self._cursor.lastrowid # Get id of post inserted above. 
        self._author.insert_into_viewed_by(postID) # Insert (UserID, PostID) into ViewedBy. 

    def get_folder_id(self):
        """Find FolderID that belongs to the folder-name given in constructor."""
        select_query = "SELECT FolderID FROM Folder WHERE Name = %s"
        self._cursor.execute(select_query, (self._folder_name, )) 

        fetched_data = self._cursor.fetchone()
    
        if not fetched_data:
            print("A folder with the name "+self._folder_name+" does not exist in the database.")
            return 

        self._folder_id = fetched_data[0]
        return self._folder_id

    def __del__(self):
        print("Make_post del has been called!")
        self._cursor.close() # Each object's cursor is closed when program terminates. 
