import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'dbprojectuser',
  'password': 'admin',
  'host': '127.0.0.1',
  'database': 'DB1Project',
  'raise_on_warnings': True
}
"""

# Open connection with error-catching. 
try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
"""
cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

insertion = "insert into User values (%s, %s, %s, %s, %s, %s)"
values = [(int(1), "Alex", "Johrt", "alex@test.com", "12345", "student"), 
          (int(2), "Jim", "Gull", "jimmern@test.com", "123456", "instructor"), 
          (int(3), "Molder", "Skog", "molderskog@test.com", "123456", "instructor")]

cursor.executemany(insertion, values)

cnx.commit() # Make sure inserted data is committed to the db.

select_query = "SELECT * FROM User"

cursor.execute(select_query)

for usr in cursor.fetchall():
    print(usr)

cursor.close()
cnx.close()
