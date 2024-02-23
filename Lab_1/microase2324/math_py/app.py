from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
import requests, time, os, threading
from datetime import datetime
import random
import operator
from functools import reduce

LOG_URL = 'http://log-service:5000'

app = Flask(__name__, instance_relative_config=True)

@app.errorhandler(Exception)
def handle_exception(e):
    os._exit(0)

def get_input_and_compute(op, name):
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    lst = request.args.get('lst', type=str)
    if lst is not None:
        #lst = eval(lst) # get list from string
        import ast
        ast.literal_eval(lst)
        if (op in [operator.truediv, operator.mod]) and any(x == 0 for x in lst[1:]):
            return make_response('Cannot divide by zero\n', 400)
        value = reduce(op, lst)
        sendLog("reduce with",lst,name,value,request.host)
        return value
    sendLog(a,b,'+',a+b,request.host)
    return op(a,b)

@app.route('/add')
def add():
    value = get_input_and_compute(operator.add, "+")
    return make_response(jsonify(s=value), 200)
    
@app.route('/sub')
def sub():
    value = get_input_and_compute(operator.sub, "-")
    return make_response(jsonify(s=value), 200)

@app.route('/mul')
def mul():
    value = get_input_and_compute(operator.mul, "*")
    return make_response(jsonify(s=value), 200)

@app.route('/div')
def div():
    value = get_input_and_compute(operator.truediv, "/")
    return make_response(jsonify(s=value), 200)

@app.route('/mod')
def mod():
    value = get_input_and_compute(operator.mod, "%")
    return make_response(jsonify(s=value), 200)

@app.route('/secure_random')
def secure_random(): # is it really secure?
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 0, type=float)
    a = int(a)
    b = int(b)
    #value = random.randint(a,b)
    if a > b:
        a, b = b, a
    import secrets
    value = secrets.randbelow(b-a+1) + a
    sendLog(a,b,'randint', value,request.host)
    
    return make_response(jsonify(s=value), 200)

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

def sendLog(a,b,op,res,URL):
    try:
        s = str(a) + ' ' + str(op) + ' ' + str(b) + ' = ' + str(res) + " _from: "+URL
        x = requests.post(LOG_URL + f'/addLog',json={'time':str(datetime.now()), 'log':s})
        x.raise_for_status()
    except (ConnectionError, HTTPError):
        return 