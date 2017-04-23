from connection import *
from all_user import *
from datetime import datetime

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
	def changeDP_one(self, date_time, location, state):
		connection = connect()
		status = 'Accepted' if state else 'Rejected'
		cursor = connection.cursor()
		sql = "UPDATE Data_Point SET Status = %s WHERE LocName = %s AND DateTime = %s"
		cursor.execute(sql, (status, location, date_time))
		result = cursor.fetchall()
		print '\nAfter change:'
		print result
		connection.commit()
		connection.close()

	def changeDP(self, keys, state):
		connection = connect()

		for key in keys:
			newtime = datetime.strptime(key['DateTime'], '%a, %d %b %Y %H:%M:%S %Z')
			date, time = str(newtime.date()), str(newtime.time())
			key['DateTime'] = date + ' ' + time[0:5]

		status = 'Accepted' if state else 'Rejected'

		sql = "UPDATE Data_Point SET Status = \'{0}\' WHERE (LocName = \'{1}\' AND DateTime = \'{2}\')".format(status, keys[0]["LocName"], keys[0]["DateTime"])

		if len(keys) == 1:
			sql = sql
		else:
			for i in range(1, len(keys)):
				sql = sql + " OR (LocName = \'{0}\' AND DateTime = \'{1}\')".format(keys[i]["LocName"], keys[i]["DateTime"])

		cursor = connection.cursor()

		cursor.execute(sql)

		connection.commit()
		connection.close()


	def changeCOA_one(self, email, status):
		# status = 'Accepted' if s else 'Rejected'
		connection = connect()
		cursor = connection.cursor()
		sql = "UPDATE City_Official SET Status = %s WHERE EmailAddress = %s"
		# cursor.execute(sql, (status, email))
		cursor.execute(sql, (status, email))
		connection.commit()
		connection.close()
		print "changed status for ", email

	#change status of city official account
	# def changeCOA(self, index, results, state):
	# 	connection = connect()
	# 	if state == 1:
	# 		status = 'Approved'
	# 	else:
	# 		status = 'Rejected'

	# 	for i in index:
	# 		cursor = connection.cursor()
	# 		sql = "UPDATE City_Official SET Status = %s WHERE EmailAddress = %s"

	# 		key = (results[i])["EmailAddress"]

	# 		cursor.execute(sql, (status, key))
	# 		print '\nBefore change:'
	# 		print results[i]


	# 		cursor = connection.cursor()
	# 		sql = "SELECT EmailAddress, Status FROM City_Official WHERE EmailAddress = %s"
	# 		cursor.execute(sql, key)
	# 		result = cursor.fetchone()
	# 		print '\nAfter Change:'
	# 		print result
	# 	connection.commit()
	# 	connection.close()

if __name__ == "__main__":
	# test = LogIn()
	test1 = Admin()
	# test.deleteUser('Oprah Winfrey')
	# print test.checkUniqueName('Justin Bieber')
	# print test.register('Oprah Winfrey','Oprah.Winfrey@gatech.edu', 'OprahWinfrey','OprahWinfrey', 'City Official', 'Major', 'Jacksonville', 'Florida')
	# print test1.pendingCOA()
	# test1.changeCOA_one('Oprah.Winfrey@gatech.edu', 1)
	# print test1.pendingCOA()
    #

	test1.changeDP([['Georgia Tech', '2017-03-31 15:37'], ['Georgia Tech', '2017-03-31 15:36']], 1)
