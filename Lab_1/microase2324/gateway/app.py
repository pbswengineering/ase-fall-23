import requests

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from urls import *
import redis

ALLOWED_MATH_OPS = ['add', 'sub', 'mul', 'div', 'mod', 'crash']
ALLOWED_STR_OPS = ['lower', 'upper', 'concat', 'crash']

ids = {} #CAREFUL, THIS IS NOT FOR MULTIUSER AND MULTITHREADING, JUST FOR DEMO PURPOSES

app = Flask(__name__, instance_relative_config=True)

r = redis.Redis(host='db', port=6379, decode_responses=True)

def create_app():
    return app

@app.route('/math/<op>')
def math(op):
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if op not in ALLOWED_MATH_OPS:
        return make_response('Invalid operation\n', 404)
    try:
        M_URL=getMathURL()
        if({op} == 'crash'):
            URL = M_URL + f'/crash'
        else:
            URL = M_URL + f'/{op}?a={a}&b={b}'
        x = requests.get(URL)
        x.raise_for_status()
        res = x.json()
        return res
    except (ConnectionError):
        try:
            M_URL=getMathURL()
            if({op} == 'crash'):
                URL = M_URL + f'/crash'
            else:
                URL = M_URL + f'/{op}?a={a}&b={b}'
            x = requests.get(URL)
            x.raise_for_status()
            res = x.json()
        except ConnectionError:
            return make_response('Math service is down\n', 404)
        except HTTPError:
            return make_response('Invalid input\n', 400)

        return res


def getMathURL():
    id = ids.get('id')
    if id is None:
        id = 0
    id = id + 1
    ids.update({'id':id})
    if id %2 == 0:
        return MATH_URL
    else:
        return MATH2_URL

@app.route('/str/<op>')
def string(op):
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if op not in ALLOWED_STR_OPS:
        return make_response('Invalid operation\n', 404)
    try:
        if op == 'lower' or op == 'upper':
            x = requests.get(STRING_URL + f'/{op}?a={a}')
        elif op == 'crash':
            x = requests.get(STRING_URL + f'/crash')
        else:
            x = requests.get(STRING_URL + f'/{op}?a={a}&b={b}')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('String service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

@app.route('/log/<op>')
def log(op):
    if op == 'getLogs':
        return getLogs()
    elif op == 'crash':
        return crashLog()
    else:
        return make_response('Invalid operation\n', 404)

def crashLog():
    try:
        x = requests.get(LOG_URL + f'/crash')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Log service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

def getLogService():
    try:
        x = requests.get(LOG_URL + f'/getLogs')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Log service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

def getLogDB():
    res = {}
    for key in r.scan_iter(match="*"):
        value = r.get(key)
        res.update({key : value})
    return make_response(jsonify(res), 200)



def getLogs():
    return getLogService()