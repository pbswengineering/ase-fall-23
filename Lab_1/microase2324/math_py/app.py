from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
import requests, time, redis, os, threading
from datetime import datetime

LOG_URL = 'http://log-service:5000'

app = Flask(__name__, instance_relative_config=True)
r = redis.Redis(host='db', port=6379, decode_responses=True)

@app.errorhandler(Exception)
def handle_exception(e):
    os._exit(0)

@app.route('/add')
def add():
    a = request.args.get('a', 0,type=float)
    b = request.args.get('b', 0,type=float)
    sendLog(a,b,'+',a+b,request.host)
    return make_response(jsonify(s=a+b), 200)
    
@app.route('/sub')
def sub():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    sendLog(a,b,'-',a-b,request.host)
    return make_response(jsonify(s=a-b), 200)

@app.route('/mul')
def mul():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    sendLog(a,b,'*',a*b,request.host)
    return make_response(jsonify(s=a*b), 200)

@app.route('/div')
def div():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    if b == 0:
        return make_response('Cannot divide by zero\n', 400)
    else:
        sendLog(a,b,'/',a/b,request.host)
        return make_response(jsonify(s=a/b), 200)

@app.route('/mod')
def mod():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    if b == 0:
        return make_response('Cannot mod by zero\n', 400)
    else:
        sendLog(a,b,'%',a%b,request.host)
        return make_response(jsonify(s=a%b), 200)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)
    

def create_app():
    return app

def sendLogDB(a,b,op,res,URL):
    s = str(a) + ' ' + str(op) + ' ' + str(b) + ' = ' + str(res) + " _from: "+URL
    r.set(str(datetime.now()), s)

def sendLogService(a,b,op,res,URL):
    s = str(a) + ' ' + str(op) + ' ' + str(b) + ' = ' + str(res) + " _from: "+URL
    x = requests.post(LOG_URL + f'/addLog',json={'time':str(datetime.now()), 'log':s})
    x.raise_for_status()
    
def sendLog(a,b,op,res,URL):
    return sendLogDB(a,b,op,res,URL)