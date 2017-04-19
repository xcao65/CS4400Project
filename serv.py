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
    return jsonify([{"name": "AQI", "id": 0}, {"name": "Mold", "id": 1}])

@app.route('/api/points', methods=["PUT"])
@check_login
def save_point():
    payload = request.get_json()
    print("save_point is called: ", payload)
    # pretend saving
    payload["id"] = 100
    return jsonify({"succ": 0, "data":payload})
    
@app.route('/api/points', methods=["POST", "GET"])
@check_login
def fetch_points():
    return jsonify(
    [
        {"loc": {"name": "Starling City"}, "attr": "AQI", "val": "31"}, 
        {"loc": {"name": "shanghai"}, "attr": "AQI", "val": "1099"}, 
        {"loc": {"name": "shanghai"}, "attr": "Flood", "val": "Tue Apr 18 20:13:59 EDT 2017"}
    ])

@app.route('/api/locations', methods=["POST", "GET"])
@check_login
def fetch_locations():
    return jsonify(
    [ {"name": "Starling City", "id": 0}
     ,{"name": "Fairview", "id": 1}
     ,{"name": "Mt. Pleasant", "id": 2}
     ,{"name": "shanghai", "id": 3}
    ])

@app.route('/api/locations', methods=["PUT"])
@check_login
def save_location():
    payload = request.get_json()
    print("save_location is called: ", payload)
    payload["id"] = 999
    return jsonify({"succ": 0, "data":payload})

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
