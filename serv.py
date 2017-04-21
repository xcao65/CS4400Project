from datetime import datetime
from functools import wraps
import os
import signal
import ssl
import sys

from flask import (
    Flask, flash, redirect, render_template, request, session, 
    abort, jsonify, escape, send_from_directory
)
import pymysql
import pymysql.cursors

from sessions import Xavier

app = Flask(__name__)
prof = Xavier()
roles = {"admin", "scientist", "official"}

def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not prof.has_login(session.get('session_id')):
            return jsonify({'succ': 6, 'msg': 'not logged in'})
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def home():
    if session.get('session_id') and prof.has_login(session.get('session_id')):
        return redirect("index.html")
    else:
        return redirect("login.html")

@app.route('/<path:path>')
def send_static(path):
    print("Someone is up to something! ")
    if not session.get('session_id'): # inject session id
        print("Injecting session_id..")
        session['session_id'] = prof.generate()
    if path == "index.html" and prof.has_login(session.get('session_id')):
        _, memo = prof.get(session.get('session_id'))
        if memo and "role" in memo and memo["role"] in roles:
            return send_from_directory('static', memo['role'] + ".html")
        else:
            return redirect("login.html")
    if path != "login.html" and not prof.has_login(session.get('session_id')):
        print("redirect to login")
        return redirect('login.html')
    else:
        print("sending file - " + path) 
        return send_from_directory('static', path)

@app.route('/api/login', methods=["POST"])
def do_login():
    if not session.get('session_id'): 
        return jsonify({"succ": 5, "msg": "bad session"})
    if not request.form["username"]:
        return jsonify({"succ": 6, "msg": "bad username"})
    print("login api is called, session id = " + session.get('session_id'))
    uid = request.form["username"]
    c0 = uid[0].lower()
    role = 'admin' if c0 < 'o' else ('official' if c0 <'s' else 'scientist')
    prof.put(session.get('session_id'), uid, {"role": role})
    return redirect("index.html")

@app.route('/api/logout', methods=["POST", "GET"])
def do_logout():
    if session.get('session_id'):
        prof.clear(session.get('session_id'))
    return redirect("login.html")

@app.route('/api/types', methods=["get"])
@check_login
def fetch_types():
    return jsonify({ 'succ': 0, 'c': ["AQ", "Mold"]})

@app.route('/api/points', methods=["PUT"])
@check_login
def save_point():
    payload = request.get_json()
    print("save_point is called: ", payload)
    # pretend saving
    if 'id' in payload:
        # update a data point
        pass
    else:
        payload["id"] = 100
    if 'ts' in payload: 
        print('parsed time: ', datetime.strptime(payload['ts'], '%Y-%m-%dT%H:%M'))
    return jsonify({"succ": 0, "c":payload})
    
@app.route('/api/points', methods=["POST", "GET"])
@check_login
def fetch_points():
    return jsonify({ 'succ': 0, 'c':
    [ {"loc": 0, "attr": "AQI", "val": 31, 'id': 0, 'ts': '12-08-2014', 'status': -1}
    , {"loc": 1, "attr": "AQI", "val": 1099, 'id': 3, 'ts': '04-21-2017', 'status': -1} 
    , {"loc": 1, "attr": "Mold", "val": 653, 'id': 5, 'ts': '10-02-2017', 'status': -1}
    , {"loc": 3, "attr": "Mold", "val": 9, 'id': 15, 'ts': '09-11-2015', 'status': -1}
    ]})

@app.route('/api/filter_points', methods=["POST"])
@check_login
def filter_points():
    payload = request.get_json()
    print('filter_points is called with ', payload)
    return jsonify({ 'succ': 0, 'c':
    [ {"loc": 1, "attr": "AQI", "val": 31, 'ts': '04-11-2017'}
    , {"loc": 1, "attr": "AQI", "val": 1099, 'ts': '04-12-2017'}
    , {"loc": 1, "attr": "Mold", "val": 653, 'ts': '04-18-2017'}
    , {"loc": 1, "attr": "AQI", "val": 12, 'ts': '04-22-2017'}
    , {"loc": 1, "attr": "AQI", "val": 15, 'ts': '04-23-2017'}
    ]})
    

@app.route('/api/locations', methods=["POST", "GET"])
@check_login
def fetch_locations():
    return jsonify({ 'succ': 0, 'c':
    [ {"name": "Chamblee", "id": 0, "zip": 24972, "city": 1, "state": 0, "flag": None}
     ,{"name": "Duluth", "id": 1, "zip": 42623, "city": 1, "state": 0, "flag": '04-10-2017'}
     ,{"name": "Mt. Pleasant", "id": 2, "zip": 29472, "city": 0, "state": 0, "flag": None}
     ,{"name": "Spring Rd.", "id": 3, "zip": 92742, "city": 0, "state": 1, "flag": None}
    ]})

@app.route('/api/filter_loc', methods=["POST", "GET"])
@check_login
def filter_locations():
    print('filter_locations called! ', request.get_json())
    return jsonify({ 'succ': 0, 'c':
    [ {"name": "Mt. Pleasant", "id": 2, "zip": 29472, "city": 0, "state": 0, "flag": None}
     ,{"name": "Spring Rd.", "id": 3, "zip": 92742, "city": 0, "state": 1, "flag": '04-18-2017'}
    ]})

@app.route('/api/flag', methods=["PUT"])
@check_login
def flag_loc():
    payload = request.get_json()
    print('flag called! ', payload)
    payload['flag'] = None if payload['flag'] else '05-01-2017'
    return jsonify({'succ': 0, 'c': payload})
    
@app.route('/api/city_state', methods=["GET", "POST"])
@check_login
def fetch_city_state():
    return jsonify({"succ":0, "c":[
      {"c": "New York", "s": "NY"}
    , {"c": "New York", "s": "SC"}
    , {"c": "New York", "s": "CA"}
    , {"c": "Los Angeles", "s": "CA"}
    , {"c": "Chattanooga", "s": "SC"}
    , {"c": "Atlanta", "s": "GA"}
    ]})
    
@app.route('/api/locations', methods=["PUT"])
@check_login
def save_location():
    payload = request.get_json()
    print("save_location is called: ", payload)
    payload["id"] = 999
    return jsonify({"succ": 0, "c":payload})

@app.route('/api/report', methods=["POST"])
@check_login
def generate_report():
    return jsonify({'succ': 0, 'c': [
      {'id': 10, 'name': 'Georgia Tech', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 11, 'name': 'GSU', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 12, 'name': 'Tenth and Home', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 13, 'name': 'Suntrust Park', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 15, 'name': 'Pepsi Theme park', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 19, 'name': 'Chtanooga river', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    , {'id': 22, 'name': 'Westmar', 'city': 0, 'state': 1, 'min_mold': 2, 'avg_mold': 43.1, 'max_mold': 160, 'min_aq': 3, 'avg_aq': 33.4, 'max_aq': 84, 'num_points': 52, 'flag': '01-09-2017'}
    ]})
    
@app.route('/api/accounts', methods=["PUT"])
@check_login
def save_account():
    payload = request.get_json()
    print('saving account ', payload)
    if 'id' in payload:
        # update account
        pass
    else:
        # add new account
        payload.id = 2425
    return jsonify({'succ': 0, 'c': payload})
    
@app.route('/api/accounts', methods=["POST"])
@check_login
def fetch_accounts():
    print('type of accounts requested: ', request.get_json().get('type'))
    return jsonify({'succ': 0, 'c': 
    [ {'id': 9, 'name': 'Pearson', 'email': 'person@gatech.edu', 'city': 0, 'state': 0, 'title': 'Mayor', 'status': -1}
    , {'id': 3,'name': 'Sean', 'email': 'sean.scott.williams@gatech.edu', 'city': 0, 'state': 0, 'title': 'Ambassador', 'status': -1}
    , {'id': 6,'name': 'Jeff', 'email': 'jeff@georgia.gov', 'city': 0, 'state': 0, 'title': 'Secretary', 'status': -1}
    , {'id': 15,'name': 'Jen', 'email': 'jen@georgia.gov', 'city': 0, 'state': 0, 'title': 'Deputy', 'status': -1}
    ]})

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
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('etc/ssl/domain.crt', 'etc/ssl/domain.key')
    
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000, ssl_context=context)
