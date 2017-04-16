

class Admin():
	def PendingDataPoint(self, connection):
		cursor = connection.cursor()
		sql = "SELECT LocName AS POI location, DataType AS Data type, DataValue AS Data value, DateTime AS Time&date of data reading, FROM Data_Point WHERE Status = Pending"
		cursor.execute(sql)