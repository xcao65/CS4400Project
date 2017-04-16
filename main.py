import pymysql.cursors
from all_user import LogIn


connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='cs4400_Group_79',
                             password='tpyJ6PVQ',
                             db='cs4400_Group_79',
                             # charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

test = LogIn()
test.login('Justin Bieber','JustinBieber', connection)
# It will print
# Congrats! You successfully logged in
# City Scientist
# on Screen

connection.close()
