# from connection import *
from datetime import datetime

class CityOfficial():
	def applyFilter(self, name, city, state, zipc, flag, dateFlag, connection):
		# connection = connect()
		cursor = connection.cursor()
		if name == None:
			name = "LocationName"

		if city == None:
			city = "City"

		if state == None:
			state = "State"

		if zipc == None:
			zipc = "ZipCode"

		if flag == None:
			flag = "Flag"

		Formalized_Date = []

		if dateFlag == None:
			Formalized_Date = ""
		else:	
			# Assume time format: Date: yyyy/mm/dd ; Time: hh:mm AS STRING
			for i in range(0,2):
				Date = dateFlag[i].split('/')
				Date = map(int, Date)
				# Convert the format into yyyy-mm-dd hh:mm
				Formalized_Date.append(datetime(*Date).strftime('%Y-%m-%d'))


		sql = "SELECT * FROM POI WHERE LocationName = %s AND City = %s AND State = %s AND ZipCode = %s AND Flag = %s AND DateFlagged BETWEEN %s AND %s" 
		# cursor.execute(sql, (city, state, zipc, flag, Formalized_Date[0], Formalized_Date[1]))
		cursor.execute(sql, (name, city, state, zipc, flag, Formalized_Date[0], Formalized_Date[1]))
		results = cursor.fetchone()
		print results

		# connection.commit()
		connection.close()

	def showPOIDetail(self, locname, dataType, dataValue, date, time, connection):
		cursor = connection.cursor()
		
		Formalized_DateTime = []

		for i in range(0,2):

			DateTime = date[i].split('/') + time[i].split(':')
			DateTime = map(int, DateTime)
			# Convert the format into yyyy-mm-dd hh:mm
			Formalized_DateTime.append(datetime(*DateTime).strftime('%Y-%m-%d %H:%M'))

		sql = "SELECT DataType, DataValue, DateTime FROM Data_Point WHERE LocName = %s AND DataType = %s AND DataValue BETWEEN %s AND %s AND DateTime BETWEEN %s AND %s"
		print Formalized_DateTime
		cursor.execute(sql, (locname, dataType, dataValue[0], dataValue[1], Formalized_DateTime[0], Formalized_DateTime[1]))
		results = cursor.fetchall()
		print results
		
		connection.close()

