from datetime import datetime
from connection import *
from checks import *

################
# Test only
import pymysql
import pymysql.cursors



class CityScientist():

	# Allow city scientists to add new location to the POI table.
	def addNewLocation(self, locationname, city, state, zipcode):

		# Need to be implemented: check the format of ZipCode
		connection = connect()
		try:
			with connection.cursor() as cursor:
				# Construct the SQL expression
				sql = "INSERT INTO POI (Flag, LocationName, ZipCode, City, State) VALUES (%s, %s, %s, %s, %s)"

				# MySQL automatically set False = 0, True = 1. So explicitly change the first variable
				init_data = (0, locationname, zipcode, city, state)
				cursor.execute(sql, init_data);

				# Get the response from DB
				result = cursor.fetchone()
				if result is not None:
					raise Exception("Bad response in addNewLocation - CityScientist!", result)
				else:
					connection.commit()
		# except ExceptionType, Argument:
		#		print "Type:%s , %s  in addNewLocation of CityScientist!" % (ExceptionType, Argument)
		finally:
			if connection:
				connection.close()


	# Allow city scientists to
	def addNewDataPoint(self, locationname, date, time, datatype, value):

		# Need to be implemented: Check format of Data, Time, type of value

		# if type(value) is not int:
		if not isinstance(value, int):
			print "Wrong type of DataValue: should be INT, now %s" % type(value)
			return

		connection = connect()
		try:
			with connection.cursor() as cursor:
				# Construct the SQL expression. Use default value for Status (e.g. "Pending").
				sql = "INSERT INTO Data_Point (DateTime, LocName, DataType, DataValue) VALUES (%s, %s, %s, %s)"

				# Assume time format: Date: yyyy/mm/dd ; Time: hh:mm AS STRING
				DateTime = date.split('/') + time.split(':')
				DateTime = map(int, DateTime)
				# Convert the format into yyyy-mm-dd hh:mm
				Formalized_DateTime = datetime(*DateTime).strftime('%Y-%m-%d %H:%M')

				init_data = (Formalized_DateTime, locationname, datatype, value)
				cursor.execute(sql, init_data);

				# Get the response from DB
				result = cursor.fetchone()
				if result is not None:
					raise Exception("Bad response in addNewDataPoint of CityScientist!", result)
				else:
					connection.commit()
				connection.commit()
		# except ExceptionType, Argument:
		#		print "Type:%s , %s  in addNewDataPoint of CityScientist!" % (ExceptionType, Argument)
		finally:
			if connection:
				connection.close()


################
# Test only
# connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
#                              user='cs4400_Group_79',
#                              password='tpyJ6PVQ',
#                              db='cs4400_Group_79',
#                              # charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# scientistTest = CityScientist()
# # scientistTest.addNewLocation("ddd", "Atlanta", "Georgia", "30318", connection)
# scientistTest.addNewDataPoint("ccc", "1999/03/04", "05:06", "Mold", 666, connection)
