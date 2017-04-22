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



		# if name == None:
		# 	name = "LocationName"

		# if city == None:
		# 	city = "City"

		# if state == None:
		# 	state = "State"

		# if zipCode == None:
		# 	zipCode = "ZipCode"

		# if flag == None:
		# 	flag = "Flag"

		Formalized_Date = ['1','2']

		if dateFlag == None:
			Formalized_Date = ""
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

		connection.commit()
		connection.close()

#	def showDetail():
