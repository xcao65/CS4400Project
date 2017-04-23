import pymysql
import pymysql.cursors
import os
from connection import *
from decimal import *

class POIreport(object):

	def generateReport(self):
		sql = ''
		# with open('/Users/xuxueyang/Desktop/query.txt') as f:
		with open("POIReportQuery.txt") as f:
			# line = f.readline()
			# if line != '\n':
			# 	sql  = sql + " " + line
			sql = f.read().replace('\n',' ')
		# print sql

		connection = connect()
		with connection.cursor() as cursor:
			cursor.execute(sql)
			results = cursor.fetchall()

		# print results
		# for i in results:
		# 	print i

		# connection.commit()
		connection.close()

		if results is not None:
			for dic in results:
				dic['id'] = results.index(dic)
				dic['name'] = dic.pop(u'LocationName')
				dic['city'] = dic.pop(u'City')
				dic['state'] = dic.pop(u'State')
				dic['min_mold'] = dic.pop(u'MoldMin') if dic[u'MoldMin'] else 'None'

				if dic[u'MoldAvg'] is not None:
					dic['avg_mold'] = float(dic.pop(u'MoldAvg'))
				else:
					# dic['avg_mold'] = dic.pop(u'MoldAvg')
					dic['avg_mold'] = 'None'

				dic['max_mold'] = dic.pop(u'MoldMax') if dic[u'MoldMax'] else 'None'
				dic['min_aq'] = dic.pop(u'AQMin') if dic[u'AQMin'] else 'None'

				if dic[u'AQAvg'] is not None:
					dic['avg_aq'] = float(dic.pop(u'AQAvg'))
				else:
					# dic['avg_aq'] = dic.pop(u'AQAvg')
					dic['avg_aq'] = 'None'

				dic['max_aq'] = dic.pop(u'AQMax') if dic[u'AQMax'] else 'None'
				dic['num_points'] = dic.pop(u'numOfDataPoint') if dic[u'numOfDataPoint'] else 'None'
				dic['flag'] = dic.pop(u'DateFlagged')

# 'id': 10, 'name': 'Georgia Tech', 'city': 0,
# 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160,
# 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}

# {u'City': 'Austin', u'MoldMin': 12344, u'State': 'Texas',
#  u'MoldAvg': Decimal('12344.0000'), u'AQMax': None, u'LocationName': '1111',
#   u'numOfDataPoint': 1, u'POIlocation': '1111', u'AQMin': None, u'MoldMax': 12344,
#   u'Flag': 0, u'AQAvg': None}

		print results
		return results

if __name__ == '__main__':
	test = POIreport()
	test.generateReport()
