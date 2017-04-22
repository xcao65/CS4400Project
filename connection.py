import pymysql

def connect():
    try:
        connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                     user='cs4400_Group_79',
                                     password='tpyJ6PVQ',
                                     db='cs4400_Group_79',
                                     # charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except:
        messagebox.showwarning('Error','Please check internet connection')
