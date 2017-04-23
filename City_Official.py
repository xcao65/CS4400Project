# from connection import *
from datetime import datetime
from connection import *

class CityOfficial():

	def applyFilter(self, name, city, state, zipCode, flag, dateFlag):
		connection = connect()
		cursor = connection.cursor()

		isFirstCondition = True

		if name == None and city == None and state == None and zipCode == None and flag == None and dateFlag == [None, None]:
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


		Formalized_Date = ["DateFlagged", "DateFlagged"]

		if dateFlag == [None, None]: # or maybe [None, None] ?
			sql = sql
		else:
			# Assume time format: Date: yyyy/mm/dd ; Time: hh:mm AS STRING
			for i in range(len(dateFlag)):
				if dateFlag[i] is not None:
					Date = dateFlag[i].split('/')
					Date = map(int, Date)
					# Convert the format into yyyy-mm-dd hh:mm
					Formalized_Date[i] = (datetime(*Date).strftime('%Y-%m-%d'))
					Formalized_Date[i] = "\'%s\'" % Formalized_Date[i]

			if isFirstCondition:
				# if not (None in dateFlag):
				sql = sql + " DateFlagged >= {0} AND DateFlagged <= {1}".format(Formalized_Date[0], Formalized_Date[1])
				isFirstCondition = False
			else:
				sql = sql + " AND DateFlagged >= {0} AND DateFlagged <= {1}".format(Formalized_Date[0], Formalized_Date[1])

		# if isFirstCondition:
		# 	sql = sql + " LocationName in (SELECT DISTINCT LocName FROM Data_Point WHERE Status = 'Accepted')"
		# 	isFirstCondition = False
		# else:
		# 	sql = sql + " AND LocationName in (SELECT DISTINCT LocName FROM Data_Point WHERE Status = 'Accepted')"
		#print (sql)

		# sql = "SELECT * FROM POI WHERE LocationName = %s AND City = %s AND State = %s AND ZipCode = %s AND Flag = %s AND DateFlagged BETWEEN %s AND %s"
		# sql = "SELECT * FROM POI WHERE LocationName = \'Lenox Square\'"

		cursor.execute(sql)
		# # cursor.execute(sql, (name, city, state, zipCode, flag, Formalized_Date[0], Formalized_Date[1]))
		results = cursor.fetchall()
		# return results
		connection.close()

		for result in results:
			result['DateFlagged'] = str(result['DateFlagged'])
		# print results
		# print results[0].keys()

		# Change the name of keys to make it compatible with jsonify() in serv.py
		if results is not None:
			for dic in results:
				dic['id'] = results.index(dic)
				dic['name'] = dic.pop(u'LocationName')
				dic['zip'] = dic.pop(u'ZipCode')
				dic['city'] = dic.pop(u'City')
				dic['state'] = dic.pop(u'State')
				dic['flag'] = dic.pop(u'DateFlagged')
				dic['flagged'] = dic.pop(u'Flag')

		# print results
		return results


	def showPOIDetail(self, locname, dataType, dataValue, date, time):
		# Must input input two datetime value
		connection = connect()
		cursor = connection.cursor()

		sql = "SELECT DataType, DataValue, DateTime FROM Data_Point WHERE LocName = \'{0}\'".format(locname)

		if dataType == None:
			sql = sql
		else:
			sql = sql + " AND DataType = \'{0}\'".format(dataType)

		if dataValue == [None, None]:
			sql = sql
		else:
			if dataValue[0] == None:
				dataValue[0] = 0
			if dataValue[1] == None:
				dataValue[1] = 99999999
			# Default_DataValue = ['DataValue', 'DataValue']
			# for i in range(len(dataValue)):
				# if dataValue[i] is not None:
				# 	Default_DataValue[i] = "\'%s\'" % dataValue[i]
				# 	print Default_DataValue[i]

			sql = sql + " AND DataValue >= {0} AND DataValue <= {1}".format(dataValue[0], dataValue[1])

		if date == None:
			sql = sql
		else:
			Formalized_DateTime = ["DateTime", "DateTime"]
			for i in range(len(date)):
				if date[i] is not None:
					DateTime = date[i].split('/') + time[i].split(':')
					DateTime = map(int, DateTime)
					# Convert the format into yyyy-mm-dd hh:mm
					Formalized_DateTime[i] = (datetime(*DateTime).strftime('%Y-%m-%d %H:%M'))
					Formalized_DateTime[i] = "\'%s\'" % Formalized_DateTime[i]

			sql = sql + " AND DateTime >= {0} AND DateTime <= {1}".format(Formalized_DateTime[0], Formalized_DateTime[1])

		sql = sql + " AND Status = 'Accepted' ORDER BY DateTime"

		# print sql
		cursor.execute(sql)
		results = cursor.fetchall()
		# print results
		connection.close()

		if results is not None:
			for dic in results:
				# dic['id'] = results.index(dic)
				dic['attr'] = dic.pop(u'DataType')
				dic['val'] = dic.pop(u'DataValue')
				dic['ts'] = dic.pop(u'DateTime')
				dic['loc'] = locname

		# print results
		return results


	def flagPOI(self, locname, status):
		connection = connect()
		cursor = connection.cursor()

		# get current time
		dateFlagged = "{0}".format(datetime.now())
		dateFlagged = dateFlagged.split(' ')

		dateFlagged = dateFlagged[0] if status else 'NULL'

		if status:
			sql = "UPDATE POI SET Flag = \'{0}\', DateFlagged = \'{1}\' WHERE LocationName = \'{2}\'".format(status, dateFlagged, locname)
		else:
			sql = "UPDATE POI SET Flag = \'{0}\', DateFlagged = NULL WHERE LocationName = \'{1}\'".format(status, locname)
		# sql = "UPDATE POI SET DateFlagged = \'{0}\' WHERE LocationName = \'{1}\'".format(dateFlagged, locname)

		cursor.execute(sql)

		connection.commit()
		connection.close()

		if dateFlagged != 'NULL':
			return dateFlagged
		else:
			return None
