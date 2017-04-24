from datetime import datetime
from functools import wraps
import os
import signal
import ssl
import sys


from all_user import LogIn
from Admin import Admin
from city_state import *
from City_Scientist import CityScientist
from City_Official import CityOfficial
from POI_Report import POIreport
from checks import *

from flask import (
    Flask, flash, redirect, render_template, request, session,
    abort, jsonify, escape, send_from_directory
)
import pymysql
import pymysql.cursors

app = Flask(__name__)
t2r = {"Admin":"admin", "City Scientist":"scientist", "City Official": "official"}
t2i = {"admin":1, "scientist":2, "official": 3}

def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' not in session or not session['login'][1]:
            return jsonify({'succ': 6, 'msg': 'not logged in'})
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    role = session['login'][1] if 'login' in session else None
    return redirect((role if role else 'login') + '.html')

@app.route('/<path:path>')
def send_static(path):
    print("Someone wants {}".format(path))
    if path == "error.html":
        print("sending error page file - " + path)
        return send_from_directory('static', path)
    elif path != "login.html" and path[-5:] == '.html' and \
            ('login' not in session or not session['login'][1]):
        print("redirect to error")
        return redirect('login.html')
    else:
        print("sending file - " + path)
        return send_from_directory('static', path)

@app.route('/api/login', methods=["POST"])
def do_login():
    if not request.form["username"] or not request.form["password"]:
        return jsonify({"succ": 6, "msg": "blank username or pasword"})
    uid = request.form["username"]
    print("login api is called, username = {}".format(uid))
    # call all_user login functions
    user_type = LogIn().login(uid, request.form["password"])
    role = t2r[user_type] if user_type in t2r else None
    print("user type = {}, role = {}".format(user_type, role))
    session['login'] = (uid, role)
    return redirect((role or 'error') + ".html")

@app.route('/api/logout', methods=["POST", "GET"])
def do_logout():
    session.pop('login', None)
    return redirect("login.html")

@app.route('/api/types', methods=["get"])
@check_login
def fetch_types():
    results = import_type()
    # return jsonify({ 'succ': 0, 'c': ["AQ", "Mold"]})
    return jsonify({ 'succ': 0, 'c': results})

@app.route('/api/points', methods=["PUT"])
@check_login
def save_point():
    payload = request.get_json()
    print("save_point is called: ", payload)
    # {u'loc': u'Chastain Park', u'ts': u'2017-03-19T16:00', u'val': 111, u'attr': u'Air Quality'})
    # DateTime	LocName	Status	DataType	DataValue -- pretend saving
    # addNewDataPoint(self, locationname, date, time, datatype, value) "1999/03/04", "05:06"

    # change data point status
    # print payload: {'id': p.id, 'status': acc? 1 : 0, 'datetime': p.DateTime, 'loc': p.LocName}
    if 'id' in payload:
        # update a data points
        print('parsed time: ', datetime.strptime(payload['datetime'], '%a, %d %b %Y %H:%M:%S %Z'))
        newtime = datetime.strptime(payload['datetime'], '%a, %d %b %Y %H:%M:%S %Z')
        date, time = str(newtime.date()), str(newtime.time())
        new_date_time = date + ' ' + time
        print new_date_time
        new_admin = Admin()
        new_admin.changeDP_one(new_date_time, payload['loc'], payload['status'])
    else:
        payload["id"] = 100

    if 'ts' in payload:
        print('parsed time: ', datetime.strptime(payload['ts'], '%Y-%m-%dT%H:%M'))
        new_scientist = CityScientist()
        newtime = datetime.strptime(payload['ts'], '%Y-%m-%dT%H:%M')
        date, time = str(newtime.date()), str(newtime.time())
        date = "/".join(date.split('-'))
        time = time[0:5]
        new_scientist.addNewDataPoint(payload['loc'], date, time, payload["attr"], payload["val"])
        print "addNewDataPoint Successfully"
    return jsonify({"succ": 0, "c":payload})

@app.route('/api/points', methods=["POST", "GET"])
@check_login
def fetch_points(): # fetch pending data points
    newA = Admin()
    result = newA.pendingDP()
    '''
    return jsonify({ 'succ': 0, 'c':
    [ {"loc": 0, "attr": "AQI", "val": 31, 'id': 0, 'ts': '12-08-2014', 'status': -1}
    , {"loc": 1, "attr": "AQI", "val": 1099, 'id': 3, 'ts': '04-21-2017', 'status': -1}
    , {"loc": 1, "attr": "Mold", "val": 653, 'id': 5, 'ts': '10-02-2017', 'status': -1}
    , {"loc": 3, "attr": "Mold", "val": 9, 'id': 15, 'ts': '09-11-2015', 'status': -1}
    ]})
    '''

    return jsonify({ 'succ' : 0, 'c': result})

@app.route('/api/mark_points', methods=["POST"])
@check_login
def select_points(): #
    payload = request.get_json()
    print("select_point is called: ", payload)
    #print payload['keys'][0]
    # u'keys': [{u'LocName': u'Georgia Tech', u'DateTime': u'Tue, 31 Jan 2017 18:37:00 GMT'}]})
    if 'keys' in payload and len(payload['keys']) > 0:
        new_admin = Admin()
        new_admin.changeDP(payload['keys'], payload['acc'])
        # pass
    return jsonify({"succ": 0, "c":payload})

@app.route('/api/filter_points', methods=["POST"])
@check_login
def filter_points():
    payload = request.get_json()
    print('filter_points is called with ', payload)
    # {u'loc': 1, u'from': 0, u'attr': u'-', u'to': 10000,
    # u'flag': None, u'name': u'Emory'})
    # showPOIDetail(locname, dataType, dataValue, date, time)
    start_date, start_time, end_date, end_time = None, None, None, None
    if 'start' in payload and payload['start']!= None:
        curr_time = datetime.strptime(payload['start'], '%Y-%m-%dT%H:%M')
        start_date, start_time = '/'.join(str(curr_time.date()).split('-')), str(curr_time.time())[0:5]
        print start_date, start_time
    if 'end' in payload and payload['end']!=None:
        curr_time = datetime.strptime(payload['end'], '%Y-%m-%dT%H:%M')
        end_date, end_time = '/'.join(str(curr_time.date()).split('-')), str(curr_time.time())[0:5]
    date_range = [start_date, end_date]
    time_range = [start_time, end_time]
    value_range = [payload['from'], payload['to']]
    value_type = None if payload['attr']=='-' else payload['attr']
    new_official = CityOfficial()
    # print payload['name'], value_type, value_range, date_range, time_range
    results = new_official.showPOIDetail(payload['name'], value_type, value_range, date_range, time_range)
    # print results
    if results:
        return jsonify({"succ": 0, "c": results})
    else:
        return jsonify({"succ": 1, "c": []})
    '''
    return jsonify({ 'succ': 0, 'c':
    [ {"loc": 1, "attr": "AQI", "val": 31, 'ts': '04-11-2017'}
    , {"loc": 1, "attr": "AQI", "val": 1099, 'ts': '04-12-2017'}
    , {"loc": 1, "attr": "Mold", "val": 653, 'ts': '04-18-2017'}
    , {"loc": 1, "attr": "AQI", "val": 12, 'ts': '04-22-2017'}
    , {"loc": 1, "attr": "AQI", "val": 15, 'ts': '04-23-2017'}
    ]})
    '''

@app.route('/api/locations', methods=["POST", "GET"])
@check_login
def fetch_locations():
    results = import_location()
    return jsonify({ 'succ': 0, 'c': results})
    ''''
    [ {"name": "Chamblee", "id": 0, "zip": 24972, "city": 1, "state": 0, "flag": None}
     ,{"name": "Duluth", "id": 1, "zip": 42623, "city": 1, "state": 0, "flag": '04-10-2017'}
     ,{"name": "Mt. Pleasant", "id": 2, "zip": 29472, "city": 0, "state": 0, "flag": None}
     ,{"name": "Spring Rd.", "id": 3, "zip": 92742, "city": 0, "state": 1, "flag": None}
    ]})
    '''
@app.route('/api/filter_loc', methods=["POST", "GET"])
@check_login
def filter_locations():
    print('filter_locations called! ', request.get_json())
    payload = request.get_json()
    # {u'city': u'Atlanta', u'end': u'2012-12-12', u'name': u'- Please Select',
    # u'zip': u'111', u'start': u'2010-11-11', u'state': u'Georgia', u'flagged': True}
    # applyFilter(name, city, state, zipCode, flag, dateFlag) YYYY/MM/DD
    start_time, end_time = None, None
    if 'start' in payload:
        start_time = '/'.join(payload['start'].split('-'))
    if 'end' in payload:
        end_time = '/'.join(payload['end'].split('-'))
    time_range = [start_time, end_time]
    non = "- Please Select"
    name = None if payload['name']==non else payload['name']
    city = None if payload['city']==non else payload['city']
    state = None if payload['state']==non else payload['state']
    zip_code = None if 'zip' not in payload else payload['zip']
    flag = 1 if 'flagged' in payload and payload['flagged'] else None
    new_official = CityOfficial()
    results = new_official.applyFilter(name, city, state, zip_code, flag, time_range)
    print "returned locations are: ", results
    if results:
        return jsonify({'succ': 0, 'c': results})
    else:
        return jsonify({'succ': 1, 'c': []})
    '''
    return jsonify({ 'succ': 0, 'c':
    [ {"name": "Mt. Pleasant", "id": 2, "zip": 29472, "city": 0, "state": 0, "flag": None}
     ,{"name": "Spring Rd.", "id": 3, "zip": 92742, "city": 0, "state": 1, "flag": '04-18-2017'}
    ]})
    '''
    #return jsonify({'succ': 1, 'c': []})

@app.route('/api/flag', methods=["PUT"])
@check_login
def flag_loc():
    payload = request.get_json()
    print('flag called! ', payload)
    name = payload['name']
    # print 'before change, payload flag is ', payload['flag']
    status = 0 if payload['flagged'] else 1
    # payload['flag'] = None if payload['flag'] else '05-01-2017'
    new_official = CityOfficial()
    result = new_official.flagPOI(name, status)
    print "date flagged is ", result
    payload['flag'] = result
    payload['flagged'] = 1 if result else 0
    print 'after flag payload is ', payload
    return jsonify({'succ': 0, 'c': payload})

@app.route('/api/city_state', methods=["GET", "POST"])
# @check_login # allow registration to retrieve city_state
def fetch_city_state():
    results = import_city_state()
    return jsonify({'succ':0, "c": results})
    '''
    return jsonify({"succ":0, "c":[
      {"c": "New York", "s": "NY"}
    , {"c": "New York", "s": "SC"}
    , {"c": "New York", "s": "CA"}
    , {"c": "Los Angeles", "s": "CA"}
    , {"c": "Chattanooga", "s": "SC"}
    , {"c": "Atlanta", "s": "GA"}
    ]})
    '''

@app.route('/api/locations', methods=["PUT"])
@check_login
def save_location():
    payload = request.get_json()
    print("save_location is called: ", payload)
    # {u'city': u'Atlanta', u'state': u'Georgia', u'name': u'111', u'zip': u'111'})
    # addNewLocation(self, locationname, city, state, zipcode)
    if 'zip' in payload and validateZipCode(payload["zip"]):
        newS = CityScientist()
        newS.addNewLocation(payload["name"],payload["city"],payload["state"],payload["zip"])
        payload["id"] = 999
        return jsonify({"succ": 0, "c":payload})
    else:
        payload["id"] = 400
        return jsonify({"succ": 1, "c":payload})


@app.route('/api/report', methods=["POST"])
@check_login
def generate_report():
    results = POIreport().generateReport()
    return jsonify({'succ': 0, 'c': results})
    '''
    return jsonify({'succ': 0, 'c': [
      {'id': 10, 'name': 'Georgia Tech', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 11, 'name': 'GSU', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 12, 'name': 'Tenth and Home', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 13, 'name': 'Suntrust Park', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 15, 'name': 'Pepsi Theme park', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 19, 'name': 'Chtanooga river', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 22, 'name': 'Westmar', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    ]})
    '''

@app.route('/api/accounts', methods=["PUT"])
@check_login
def save_account():
    payload = request.get_json()
    print('saving account [accept / reject]', payload)
    # {'id': p.id, 'status': acc? 1 : 0, 'email': p.EmailAddress}
    if 'id' in payload: # currently only for accpet or reject accounts
        # pass
        new_admin = Admin()
        new_admin.changeCOA_one(payload['email'], payload['status'])
    else:
        pass # won't reach here for this assignment
    return jsonify({'succ': 0, 'c': payload})

@app.route('/api/register', methods=["GET"])
# no need to check login
def check_availability():
    print("check available? ", request.args["username"])
    return {'succ': 1, 'c': request.args["username"]}

@app.route('/api/register', methods=["POST"])
# no need to check login
def create_user():
    # add new account
    payload = request.get_json()
    print('Register for new user ', payload)
    # {u'username': u'111', u'city': u'- Please Select',
    # u'conf_pwd': u'111', u'state': u'- Please Select',
    # u'password': u'111', u'type': u'scientist', u'email': u'111@gmail.com'})
    # (name, email, pwd, cpwd, utype, *others)
    new_user = LogIn()
    user_type = payload['type']
    result = None
    if user_type == 'scientist':
        result = new_user.register(payload['username'], payload['email'], \
        payload['password'], payload['conf_pwd'], t2i[user_type])
    else:
        result = new_user.register(payload['username'], payload['email'], payload['password'], \
        payload['conf_pwd'], t2i[user_type], payload['title'], payload['city'], payload['state'])
    payload["id"] = 6666
    result = 0 if result else 1
    print "register result is ", result
    return jsonify({'succ': result, 'c': payload})

@app.route('/api/accounts', methods=["POST"])
@check_login
def fetch_accounts():
    print('type of accounts requested: ', request.get_json().get('type'))
    newA = Admin()
    results = newA.pendingCOA() # call admin functions
    return jsonify({'succ': 0, 'c': results})
    '''
    return jsonify({'succ': 0, 'c':
    [ {'id': 9, 'name': 'Pearson', 'email': 'person@gatech.edu', 'city': 0, 'state': 0, 'title': 'Mayor', 'status': -1}
    , {'id': 3,'name': 'Sean', 'email': 'sean.scott.williams@gatech.edu', 'city': 0, 'state': 0, 'title': 'Ambassador', 'status': -1}
    , {'id': 6,'name': 'Jeff', 'email': 'jeff@georgia.gov', 'city': 0, 'state': 0, 'title': 'Secretary', 'status': -1}
    , {'id': 15,'name': 'Jen', 'email': 'jen@georgia.gov', 'city': 0, 'state': 0, 'title': 'Deputy', 'status': -1}
    ]})
    '''

def signal_handler(signal, frame):
    print('Closing SQL connection...')
    if connection: connection.close()
    print('SQL connection closed. Exiting...')
    sys.exit(0)

if __name__ == "__main__":
    # print(" - Connecting to mysql...")
    # connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
    #                              user='cs4400_Group_79',
    #                              password='tpyJ6PVQ',
    #                              db='cs4400_Group_79',
    #                              # charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)

    # print(" - Register SIGINT handler...")
    # signal.signal(signal.SIGINT, signal_handler)

    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('etc/ssl/domain.crt', 'etc/ssl/domain.key')

    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)#, ssl_context=context)
