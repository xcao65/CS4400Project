class Admin():

	#fetch pending data point
	def pendingDP(self, connection):
		cursor = connection.cursor()
		sql = "SELECT LocName, DataType, DataValue, DateTime FROM Data_Point WHERE Status = %s"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchall()
		print result

	#fetch pending City official accounts
	def pendingCOA(self, connection):
		cursor = connection.cursor()
		sql = "SELECT UserName, B.EmailAddress, City, State, Title FROM User AS A, City_Official AS B WHERE Status = %s AND A.EmailAddress = B.EmailAddress"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchall()
		print len(result)

	#change status of data point
	def changeDP(self, index, results, connection, bool):
		if bool == 1:
			status = 'Approved'
		else:
			status = 'Rejected'

		result = []
		cursor = connection.cursor()

		for i in index:
			sql = "UPDATE Data_Point SET Status = %s WHERE LocName = %s AND DateTime = %s"
			key1 = (results[i])["LocName"]
			key2 = (results[i])["DateTime"]
			cursor.execute(sql, status, key1, key2)
			result.add(cursor.fetchone())

		print result