from prettytable import from_db_cursor


class Statistics_ctrl():
    """Control queries and compiling of statistics from the database."""

    def __init__(self, cnx, user):
        self._cnx = cnx
        self._user_type = user.get_type()

    def compile_stats(self):
        """Queries the database for statistics and compiles them."""
        if self._user_type != 'instructor':
            raise Exception("You do not have access to statistics!")
    
        self._cursor = self._cnx.cursor(prepared=True)
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

