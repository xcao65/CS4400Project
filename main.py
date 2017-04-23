import pymysql
import pymysql.cursors
from all_user import LogIn
from Admin import Admin
from City_Official import CityOfficial


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


#test = LogIn()
# test.login('Justin Bieber','JustinBieber', connection)
# test.login('Oprah Winfrey','OprahWinfrey', connection)
# print test.checkUniqueName('Justin Bieber', connection)

#test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', connection, 'Major', 'Jacksonville', 'Florida')
# test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', connection)
# print test.checkUniqueName('Justin Bieber', connection)
# print test.checkUniqueName('Xun Cao', connection)
# test.login("", "", connection)
# It will print
# Congrats! You successfully logged in
# City Scientist
# on Screen

# test1 = Admin()
# print 'Number of Pending DP:'
# dpResult = test1.pendingDP(connection)
# print 'Change two DPs:'
# test1.changeDP([0,1], dpResult, 1, connection)

# print 'Number of Pending COA:'
# coaResult = test1.pendingCOA(connection)
# print 'Change two COAs:'
# test1.changeCOA([0],coaResult, 1, connection)

# Test CityOfficial

test = CityOfficial()
# a = test.applyFilter('Georgia Tech', 'Atlanta', 'Georgia', '30332', 1, ['1993/01/10', '2017/10/10'])
# b = test.applyFilter('Georgia Tech', 'Atlanta', 'Georgia', '30332', 1, [None, None])
print test.applyFilter(None, None, None, None, None, [None, None])

# test.showPOIDetail('Georgia Tech', None, [30,100], ['1993/01/10', '2017/10/10'], ['00:00', '22:22'])
# print test.showPOIDetail('Georgia Tech', None, [18, None], [None, None], None)

# test.flagPOI('Georgia Tech', 1)


# connection.commit()
