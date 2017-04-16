

class Admin():
	def pendingDP(self, connection):
		cursor = connection.cursor()
		sql = "SELECT LocName, DataType, DataValue FROM Data_Point WHERE Status = %s"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchone()
		print result

	def pendingCOA(self, connection):
		cursor = connection.cursor()
		sql = "SELECT UserName, B.EmailAddress, City, State, Title FROM User AS A, City_Official AS B WHERE Status = %s AND A.EmailAddress = B.EmailAddress"
		cursor.execute(sql, 'Pending')
		result = cursor.fetchall()
		print len(result)