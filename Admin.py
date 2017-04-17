class Admin():

	#fetch pending data point
	def pendingDP(self, connection):
		cursor = connection.cursor()
		sql = "SELECT LocName, DataType, DataValue, DateTime, Status FROM Data_Point WHERE Status = %s"
		cursor.execute(sql, 'Pending')

		result =cursor.fetchall()
		print len(result)
		return result

	#fetch pending City official accounts
	def pendingCOA(self, connection):
		cursor = connection.cursor()
		sql = "SELECT UserName, B.EmailAddress, City, State, Title FROM User AS A, City_Official AS B WHERE Status = %s AND A.EmailAddress = B.EmailAddress"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchall()
		print len(result)
		return result

	#change status of data point
	def changeDP(self, index, results, bool, connection):
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

	#change status of city official account
	def changeCOA(self, index, results, bool, connection):
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