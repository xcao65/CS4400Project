# from connection import *
from datetime import datetime

class CityOfficial():
	
	def applyFilter(self, name, city, state, zipCode, flag, dateFlag, connection):
		# connection = connect()
		cursor = connection.cursor()

		isFirstCondition = True

		if(name == None and city == None and state == None and zipCode == None and flag == None and dateFlag == None):
			sql = "SELECT * FROM POI"
		else:
			sql = "SELECT * FROM POI WHERE"


		if name == None:
			sql = sql
		else:
			sql = sql + " LocationName = \'{0}\'".format(name)
			isFirstCondition = False

		if city == None:
			sql = sql
		else:
			if isFirstCondition:
				sql = sql + " City = \'{0}\'".format(city)
				isFirstCondition = False
			else:
				sql = sql + " AND City = \'{0}\'".format(city)

		if state == None:
			sql = sql
		else:
			if isFirstCondition:
				sql = sql + " State = \'{0}\'".format(state)
				isFirstCondition = False
			else:
				sql = sql + " AND State = \'{0}\'".format(state)

		if zipCode == None:
			sql = sql
		else:
			if isFirstCondition:
				sql = sql + " ZipCode = \'{0}\'".format(zipCode)
				isFirstCondition = False
			else:
				sql = sql + " AND ZipCode = \'{0}\'".format(zipCode)

		if flag == None:
			sql = sql
		else:
			if isFirstCondition:
				sql = sql + " Flag = {0}".format(flag)
				isFirstCondition = False
			else:
				sql = sql + " AND Flag = {0}".format(flag)

		Formalized_Date = ['1','2']

		if dateFlag == None:
			sql = sql
		else:	
			# Assume time format: Date: yyyy/mm/dd ; Time: hh:mm AS STRING
			for i in range(0,2):
				Date = dateFlag[i].split('/')
				Date = map(int, Date)
				# Convert the format into yyyy-mm-dd hh:mm
				Formalized_Date[i] = datetime(*Date).strftime('%Y-%m-%d')

			if isFirstCondition:
				sql = sql + " DateFlagged BETWEEN \'{0}\' AND \'{1}\'".format(Formalized_Date[0], Formalized_Date[1])
				sFirstCondition = False
			else:
				sql = sql + " AND DateFlagged BETWEEN \'{0}\' AND \'{1}\'".format(Formalized_Date[0], Formalized_Date[1])

		print (sql)

		# sql = "SELECT * FROM POI WHERE LocationName = %s AND City = %s AND State = %s AND ZipCode = %s AND Flag = %s AND DateFlagged BETWEEN %s AND %s" 
		# sql = "SELECT * FROM POI WHERE LocationName = \'Lenox Square\'" 

		cursor.execute(sql)

		# # cursor.execute(sql, (name, city, state, zipCode, flag, Formalized_Date[0], Formalized_Date[1]))
		results = cursor.fetchall()
		print results

		connection.close()



	def showPOIDetail(self, locname, dataType, dataValue, date, time, connection):
		# Must input input two datetime value

		cursor = connection.cursor()
		
		isFirstCondition = True

		sql = "SELECT DataType, DataValue, DateTime FROM Data_Point WHERE LocName = \'{0}\'".format(locname)
		

		if dataType == None:
			sql = sql
		else:
			sql = sql + " AND DataType = \'{0}\'".format(dataType)

		if dataValue == None:
			sql = sql
		else:
			sql = sql + " AND DataValue BETWEEN \'{0}\' AND \'{1}\'".format(dataValue[0], dataValue[1])

		if date == None:
			sql = sql
		else:
			Formalized_DateTime = []
			for i in range(0,2):
				DateTime = date[i].split('/') + time[i].split(':')
				DateTime = map(int, DateTime)
				# Convert the format into yyyy-mm-dd hh:mm
				Formalized_DateTime.append(datetime(*DateTime).strftime('%Y-%m-%d %H:%M'))
			sql = sql + " AND DateTime BETWEEN \'{0}\' AND \'{1}\'".format(Formalized_DateTime[0], Formalized_DateTime[1])

		sql = sql + " ORDER BY DateTime"
		print sql
		cursor.execute(sql)
		
		results = cursor.fetchall()
		print len(results)

		connection.close()

	def flagPOI(self, locname, connection):
		cursor = connection.cursor()

		# get current time
		dateFlagged = "{0}".format(datetime.now())
		dateFlagged = dateFlagged.split(' ')
		dateFlagged = dateFlagged[0]
		


		# sql = "UPDATE POI SET Flag = 1, DateFlagged = \'{0}\' WHERE LocName = \'{1}\'".format(dateFlagged, locname)
		sql = "UPDATE POI SET DateFlagged = \'{0}\' WHERE LocationName = \'{1}\'".format(dateFlagged, locname)
		print sql
		print locname
		print dateFlagged
		cursor.execute(sql)

		connection.close()
		
		cursor = connection.cursor()
		sql = "SELECT Flag FROM POI WHERE LocName = %s"
		cursor.execute(sql, locname)
		
		result = cursor.fetchall()
		print result

		# cursor.commit()
		connection.close()