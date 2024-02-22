from flask import Flask, request, make_response, jsonify
import requests, redis, os
from requests.exceptions import ConnectionError, HTTPError
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)


LOG_URL = 'http://log-service:5000'
r = redis.Redis(host='db', port=6379, decode_responses=True)

@app.errorhandler(Exception)
def handle_exception(e):
    os._exit(0)

def create_app():
    return app

@app.route('/crash')
def crash():
    os._exit(0)

@app.route('/concat')
def concat():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a and b:
        sendLog(a,b,'concat',a+b,request.host)
        return make_response(jsonify(s=a+b), 200) # HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) # HTTP 400 BAD REQUEST

@app.route('/upper')
def upper():
    a = request.args.get('a', 0, type=str)
    sendLog(a,None,'upper',a.upper(),request.host)
    return make_response(jsonify(s=a.upper()), 200)

@app.route('/lower')
def lower():
    a = request.args.get('a', 0, type=str)
    sendLog(a,None,'lower',a.lower(),request.host)
    return make_response(jsonify(s=a.lower()), 200)


def sendLogService(a,b,op,res,URL):
    if b is None:
        s = a + ' ' + op + ' ' + b + ' = ' + res + "_from: "+URL
    else:
        s = op + ' ' + a + ' = ' + res + "_from: "+URL
    x = requests.post(LOG_URL + f'/addLog',json={'time':str(datetime.now()), 'log':s})
    x.raise_for_status()


def sendLogDB(a,b,op,res,URL):
    if b is None:
            s = a + ' ' + op + ' ' + b + ' = ' + res + "_from: "+URL
    else:
            s =  ' ' + op + ' ' + a + ' = ' + res + "_from: "+URL
    r.set(str(datetime.now()), s)

def sendLog(a,b,op,res,URL):
    return sendLogDB(a,b,op,res,URL)