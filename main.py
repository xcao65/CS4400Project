import pymysql
from all_user import LogIn
from Admin import Admin


connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='cs4400_Group_79',
                             password='tpyJ6PVQ',
                             db='cs4400_Group_79',
                             # charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def deleteUser(connection, name):
    cursor = connection.cursor()
    sql = "DELETE FROM User WHERE Username =  %s "
    # cursor.execute(sql, 'Justin Bieber')
    cursor.execute(sql, name)
    connection.commit()
    print 'delete successfully'

# def deleteCityOff(connection, ):
#     cursor = connection.cursor()
#     sql = "DELETE FROM User WHERE Username =  %s "

# deleteUser(connection, 'Oprah Winfrey')


test = LogIn()
# test.login('Justin Bieber','JustinBieber', connection)
# test.login('Oprah Winfrey','OprahWinfrey', connection)
# print test.checkUniqueName('Justin Bieber', connection)

test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', connection, 'Major', 'Jacksonville', 'Florida')
# test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', connection)
# print test.checkUniqueName('Justin Bieber', connection)
# print test.checkUniqueName('Xun Cao', connection)
# test.login("", "", connection)
# It will print
# Congrats! You successfully logged in
# City Scientist
# on Screen

test1 = Admin()
test1.pendingDP(connection)
test1.pendingCOA(connection)

connection.close()
