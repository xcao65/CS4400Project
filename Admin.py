from connection import *

class Admin():

	#fetch pending data point
	def pendingDP(self):
		connection = connect()
		cursor = connection.cursor()
		sql = "SELECT LocName, DataType, DataValue, DateTime, Status FROM Data_Point WHERE Status = %s"
		cursor.execute(sql, 'Pending')

		result = cursor.fetchall()
		connection.close()
		print len(result)
		i = 0
		for dp in result:
			dp['Status'] = -1
			dp['id'] = i
			i = i+1
		return result

	#fetch pending City official accounts
	def pendingCOA(self):
		connection = connect()
		cursor = connection.cursor()
		sql = "SELECT UserName, B.EmailAddress, City, State, Title FROM User AS A, City_Official AS B WHERE Status = %s AND A.EmailAddress = B.EmailAddress"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchall()
		connection.close()
		print len(result)
		i = 0
		for dp in result:
			dp['Status'] = -1
			dp['id'] = i
			i = i+1
		return result

	#change status of data point
	def changeDP(self, index, results, bool):
		connection = connect()
		if bool == 1:
			status = 'Accepted'
		else:
			status = 'Rejected'

		for i in index:
			cursor = connection.cursor()
			sql = "UPDATE Data_Point SET Status = %s WHERE LocName = %s AND DateTime = %s"

			key1 = (results[i])["LocName"]
			key2 = (results[i])["DateTime"]
			cursor.execute(sql, (status, key1, key2))
			print '\nBefore change:'
			print results[i]
			cursor = connection.cursor()
			sql = "SELECT DateTime, Status FROM Data_Point WHERE LocName = %s AND DateTime = %s"
			cursor.execute(sql, (key1, key2))
			result = cursor.fetchone()
			print '\nAfter change:'
			print result
		connection.commit()
		connection.close()


	#change status of city official account
	def changeCOA(self, index, results, bool):
		connection = connect()
		if bool == 1:
			status = 'Approved'
		else:
			status = 'Rejected'

		for i in index:
			cursor = connection.cursor()
			sql = "UPDATE City_Official SET Status = %s WHERE EmailAddress = %s"

			key = (results[i])["EmailAddress"]

			cursor.execute(sql, (status, key))
			print '\nBefore change:'
			print results[i]


			cursor = connection.cursor()
			sql = "SELECT EmailAddress, Status FROM City_Official WHERE EmailAddress = %s"
			cursor.execute(sql, key)
			result = cursor.fetchone()
			print '\nAfter Change:'
			print result
		connection.commit()
		connection.close()

if __name__ == "__main__":
    test = Admin()
    # print test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', 'Major', 'Jacksonville', 'Florida')
    # print test.checkUniqueName('Justin Bieber')
    print test.pendingCOA()
    # print test.deleteUser('Oprah Winfrey')
