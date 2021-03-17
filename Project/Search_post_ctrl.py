"""Controller to search the posts for specific keywords."""


from DB_connector import DB_connector

class Search_post_ctrl(DB_connector):

    def __init__(self, user):
        DB_connector.__init__(self)
        self._user = user 
        self._user.check_credentials() # Check credentials again (to verify that the user is allowed to search.)
        # This is perhaps not necessary when the program is more complete, but will leave it in for now. 

    def total_search(self, keyword):
        """Search through all required tables for the keyword."""
        self._keyword = keyword;

        self.search_post()
        self.search_followup()
        self.search_reply_post()
        self.search_reply_followup()

    def search_post(self):
        """Search the Post-table for the keyword. Both 'Text' and 'Summary'. Print PostID or empty list."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT PostID FROM Post WHERE Text LIKE %s or Summary LIKE %s"
        keyword = ("%" + self._keyword + "%", "%" + self._keyword + "%")
        self._cursor.execute(select_query, keyword) 

        fetched_data = self._cursor.fetchall()
        self._cursor.close() # Close the cursor when done. 

        if not fetched_data:
            print("There are no posts that contain the keyword "+self._keyword)
            print(fetched_data)
            return 
        
        print("Search in main threads: A list of PostID's that contain the keyword "+self._keyword+" is given below.")
        for val in fetched_data:
            print(val[0], end=" ")
        print()

    def search_followup(self):
        """Search the Followup-table for the keyword. Print (PostID, FollowupID) or empty list."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT PostID, FollowupID FROM Followup WHERE Text LIKE %s"
        
        self._cursor.execute(select_query, ("%" + self._keyword + "%", )) 

        fetched_data = self._cursor.fetchall()
        self._cursor.close() # Close the cursor when done. 

        if not fetched_data:
            print("There are no followups that contain the keyword "+self._keyword)
            print(fetched_data)
            return 
        
        print("Search in followups: A list of (PostID, FollowupID)'s that contain the keyword "+self._keyword+" is given below.")
        for val in fetched_data:
            print("("+str(val[0])+", "+str(val[1])+")", end=" ")
        print()

    def search_reply_post(self):
        """Search the ReplyPost-table for the keyword. Print (ReplyID, PostID) or empty list."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT ReplyID, PostID FROM ReplyPost INNER JOIN Post USING (PostID) WHERE ReplyPost.Text LIKE %s"
        
        self._cursor.execute(select_query, ("%" + self._keyword + "%", )) 

        fetched_data = self._cursor.fetchall()
        self._cursor.close() # Close the cursor when done. 
        
        if not fetched_data:
            print("There are no post/thread-replies that contain the keyword "+self._keyword)
            print(fetched_data)
            return 
        
        print("Search in replies to main threads: A list of (ReplyID, PostID)'s that contain the keyword "+self._keyword+" is given below.")
        for val in fetched_data:
            print("("+str(val[0])+", "+str(val[1])+")", end=" ")
        print()

    def search_reply_followup(self):
        """Search the ReplyFollowup-table for the keyword. Print (ReplyID, PostID, FollowupID) or empty list."""
        self._cursor = self._cnx.cursor(prepared = True)
        select_query = "SELECT ReplyID, PostID, FollowupID FROM ReplyFollowup INNER JOIN Post USING (PostID) WHERE ReplyFollowup.Text LIKE %s"
        
        self._cursor.execute(select_query, ("%" + self._keyword + "%", )) 

        fetched_data = self._cursor.fetchall()
        self._cursor.close() # Close the cursor when done. 
        print(fetched_data)
        if not fetched_data:
            print("There are no followup-replies that contain the keyword "+self._keyword)
            print(fetched_data)
            return 
        
        print("Search in replies to followups: A list of (ReplyID, PostID, FollowupID)'s that contain the keyword "+self._keyword+" is given below.")
        for val in fetched_data:
            print("("+str(val[0])+", "+str(val[1])+", "+str(val[2])+")", end=" ")
        print()
