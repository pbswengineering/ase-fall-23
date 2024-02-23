from flask import Flask, request, make_response, jsonify
import requests, os
from requests.exceptions import ConnectionError, HTTPError
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)


LOG_URL = 'http://log-service:5000'

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


def sendLog(a,b,op,res,URL):
    try:
        if b is None:
            s = a + ' ' + op + ' ' + b + ' = ' + res + "_from: "+URL
        else:
            s = op + ' ' + a + ' = ' + res + "_from: "+URL
        x = requests.post(LOG_URL + f'/addLog',json={'time':str(datetime.now()), 'log':s})
        x.raise_for_status()
    except (ConnectionError, HTTPError):
        return 
