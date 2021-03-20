"""Controller to compile some statistics."""

from prettytable import from_db_cursor

class Statistics_ctrl:
    """Control queries and compiling of statistics from the database."""

    def __init__(self, connection, user):
        self._connection = connection
        self._user_type = user.get_type()

        # Make cursor for each object. 
        self._cursor = self._connection._cnx.cursor(prepared = True)

    def compile_stats(self):
        """Queries the database for statistics and compiles them."""
        if self._user_type != 'instructor':
            raise Exception("You do not have access to statistics!")
    
        query = ( "SELECT UserID, readPosts AS 'Posts read', writtenPosts AS 'Posts written' "
                    "FROM (SELECT UserID, COUNT(PostID) AS readPosts "
                    "FROM ViewedBy RIGHT OUTER JOIN User USING (UserID) "
                    "GROUP BY UserID "
                    "ORDER BY readPosts DESC) dt1 "
                "INNER JOIN "
                    "(SELECT u.UserID, COUNT(p.UserID) AS writtenPosts "
                    "FROM Post AS p RIGHT OUTER JOIN User AS u ON p.UserID = u.UserID "
                    "GROUP BY u.UserID) dt2 USING (UserID) "
                "ORDER BY readPosts DESC, writtenPosts DESC")
        
        self._cursor.execute(query)
        stats = from_db_cursor(self._cursor)
        print(stats)
    
    def __del__(self):
        print("Statistics del has been called!")
        self._cursor.close() # Each object's cursor is closed when program terminates.    
        