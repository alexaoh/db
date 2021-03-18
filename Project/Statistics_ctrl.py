from DB_connector import DB_connector
from prettytable import from_db_cursor


class Statistics_ctrl(DB_connector):
    """Controls making a new reply to an existing post."""

    def __init__(self, user):
        DB_connector.__init__(self)
        self._user_type = user.get_type()

    def compile_stats(self):
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
                    "GROUP BY u.UserID) dt2 USING (UserID) ")
        
        self._cursor.execute(query)
        stats = from_db_cursor(self._cursor)
        print(stats)