from connection import *

def import_city_state():
    connection = connect()
    cursor = connection.cursor()
    sql = "SELECT * FROM City_State"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()
    return results


def import_location():
    connection = connect()
    cursor = connection.cursor()
    sql = "SELECT DISTINCT LocationName FROM POI"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()
    retval = []
    # for x in results:
    #    retval.append(x["LocationName"])
    #return retval
    return results

def import_locationCO():
    connection = connect()
    cursor = connection.cursor()
    sql = "SELECT DISTINCT LocName AS LocationName FROM Data_Point WHERE Status = 'Accepted'"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()
    retval = []
    # for x in results:
    #    retval.append(x["LocationName"])
    #return retval
    return results

def import_type():
    connection = connect()
    cursor = connection.cursor()
    sql = "SELECT DISTINCT Type FROM Data_Type"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()
    retval = []
    for x in results:
        retval.append(x["Type"])
    return retval


if __name__ == '__main__':
    print "city state combinations are"
    print import_city_state()
    print "location names are"
    print import_location()
    print "data types are"
    print import_type()
    print "Locations with approved data_point are"
    print import_locationCO()
