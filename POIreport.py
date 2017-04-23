import pymysql
import pymysql.cursors
import uuid
from collections import OrderedDict
import random
from connection import *

class POIreport():
	def getlocation(self):
		cursor = connection.cursor()
		sql = "SELECT LocationName,City,State FROM POI"
		cursor.execute(sql)
		result = cursor.fetchall()
		return result

	def getflag(self, connection):
		cursor = connection.cursor()
		sql = "SELECT Flag FROM POI"
		cursor.execute(sql)
		result = cursor.fetchall()
		return result

	def minMold(self, connection, location):
		cursor = connection.cursor()
		minM = []
		for i in location:
			sql = "SELECT MIN(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Mold',))
			result = cursor.fetchall()
			minM.extend(result)
		return minM

	def maxMold(self, connection, location):
		cursor = connection.cursor()
		maxM = []
		for i in location:
			sql = "SELECT MAX(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Mold',))
			result = cursor.fetchall()
			maxM.extend(result)
		return maxM

	def avgMold(self, connection, location):
		cursor = connection.cursor()
		avgM = []
		for i in location:
			sql = "SELECT AVG(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Mold',))
			result = cursor.fetchall()
			avgM.extend(result)
		return avgM

	def minAQ(self, connection, location):
		cursor = connection.cursor()
		minAQ = []
		for i in location:
			sql = "SELECT MIN(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Air Quality',))
			result = cursor.fetchall()
			minAQ.extend(result)
		return minAQ

	def maxAQ(self, connection, location):
		cursor = connection.cursor()
		maxAQ = []
		for i in location:
			sql = "SELECT MAX(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Air Quality',))
			result = cursor.fetchall()
			maxAQ.extend(result)
		return maxAQ

	def avgAQ(self, connection, location):
		cursor = connection.cursor()
		avgAQ = []
		for i in location:
			sql = "SELECT AVG(DataValue) FROM Data_Point WHERE LocName = %s AND DataType = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname, 'Air Quality',))
			result = cursor.fetchall()
			avgAQ.extend(result)
		return avgAQ

	def numofDP(self, connection, location):
		cursor = connection.cursor()
		nDP = []
		for i in location:
			sql = "SELECT COUNT(LocName) FROM Data_Point WHERE LocName = %s"
			locationname = i['LocationName']
			cursor.execute(sql, (locationname,))
			result = cursor.fetchall()
			nDP.extend(result)
		return nDP

	def assignid(self, connection, location):
		cursor = connection.cursor()
		id = []
		length = len(location)
		for i in range(length):
			#seed = random.getrandbits(32)
			#unique_sequence = uniqueid()
			result = [{'id':i}]
			#result["id"] = i
			#print result
			id.extend(result)
		return id

	def merge(self, connection):
		cursor = connection.cursor()
		mergedlist = []
		location = self.getlocation(connection)
		moldmin = self.minMold(connection,location)
		moldavg = self.avgMold(connection,location)
		moldmax = self.maxMold(connection,location)
		AQmin = self.minAQ(connection,location)
		AQavg = self.avgAQ(connection,location)
		AQmax = self.maxAQ(connection,location)
		dpnum = self.numofDP(connection,location)
		flag = self.getflag(connection)
		id = self.assignid(connection,location)

		length = len(location)
		for i in range(length):
			temp = OrderedDict()
			temp.update(id[i])
			temp.update(location[i])
			temp['name'] = temp.pop('LocationName')
			temp['city'] = temp.pop('City')
			temp['state'] = temp.pop('State')
			#temp.update(location[i])
			moldmin[i]['min_mold'] = moldmin[i].pop('MIN(DataValue)')
			temp.update(moldmin[i])
			moldavg[i]['avg_mold'] = moldavg[i].pop('AVG(DataValue)')
			temp.update(moldavg[i])
			moldmax[i]['max_mold'] = moldmax[i].pop('MAX(DataValue)')
			temp.update(moldmax[i])

			AQmin[i]['min_aq'] = AQmin[i].pop('MIN(DataValue)')
			temp.update(AQmin[i])
			AQavg[i]['avg_aq'] = AQavg[i].pop('AVG(DataValue)')
			temp.update(AQavg[i])
			AQmax[i]['max_aq'] = AQmax[i].pop('MAX(DataValue)')
			temp.update(AQmax[i])

			dpnum[i]['num_points'] = dpnum[i].pop('COUNT(LocName)')
			temp.update(dpnum[i])
			flag[i]['flag'] = flag[i].pop('Flag')
			temp.update(flag[i])
			mergedlist.append(temp)
		return mergedlist

	def sort(self, connection, sortby):
		cursor = connection.cursor()
		list = self.merge(connection)
		newlist = sorted(list, key=lambda k: k[sortby])
		return newlist


# #main
# poi = POIreport()

# connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
#                              user='cs4400_Group_79',
#                              password='tpyJ6PVQ',
#                              db='cs4400_Group_79',
#                              # charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# '''
# test1 = poi.getlocation(connection)
# print test1
# test11 = poi.assignid(connection,test1)
# print test11

# test2 = poi.minMold(connection,test1)
# print test2
# test3 = poi.avgMold(connection,test1)
# print test3
# test4 = poi.maxMold(connection,test1)
# print test4
# test5 = poi.minAQ(connection,test1)
# print test5
# test6 = poi.avgAQ(connection,test1)
# print test6
# test7 = poi.maxAQ(connection,test1)
# print test7

# test8 = poi.numofDP(connection,test1)
# print test8
# test9 = poi.merge(connection,test1,test2,test3,test4,test5,test6,test7,test8)
# print test9
# #for example, use locationname for sorting
# test10 = poi.sort(connection,test9,'LocationName')
# print test10
# '''
# test9 = poi.merge(connection)
# print test9

# test10 = poi.sort(connection,'name')
# print test10

# connection.commit()
# connection.close()
