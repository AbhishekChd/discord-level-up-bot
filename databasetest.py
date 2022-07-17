import mysql.connector
from mysql.connector import Error


print("My name is {0.user} and i am ready to go")
print("Your bot is ready")
conn = mysql.connector('test.mysql')
cur = conn.cursor()
try :
        cur.execute('CREATE TABLE rankings (rank INTEGER, user_id STRING, level INTEGER, xp INTEGER, awarded_role INTEGER, rank_role INTEGER)')
except :
        print("database exists")
conn.close()
