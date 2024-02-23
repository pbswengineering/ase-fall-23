import requests

from flask import Flask, request, make_response
from requests.exceptions import ConnectionError, HTTPError
from urls import *
import os
import subprocess # nosec

ALLOWED_MATH_OPS = ['add', 'sub', 'mul', 'div', 'mod', 'crash', 'secure_random']
ALLOWED_STR_OPS = ['lower', 'upper', 'concat', 'crash']

ids = {} #CAREFUL, THIS IS NOT FOR MULTIUSER AND MULTITHREADING, JUST FOR DEMO PURPOSES

app = Flask(__name__, instance_relative_config=True)


def create_app():
    return app

@app.route('/math/<op>')
def math(op):
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    lst = request.args.get('lst', type=str)
    if op not in ALLOWED_MATH_OPS:
        return make_response('Invalid operation\n', 404)
    try:
        M_URL=getMathURL()
        if({op} == 'crash'):
            URL = M_URL + f'/crash'
        elif lst is not None:
            URL = M_URL + f'/{op}?lst={lst}'
        else:
            URL = M_URL + f'/{op}?a={a}&b={b}'
        x = requests.get(URL, timeout=1)
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
            x = requests.get(URL, timeout=1)
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
            x = requests.get(STRING_URL + f'/{op}?a={a}', timeout=1)
        elif op == 'crash':
            x = requests.get(STRING_URL + f'/crash', timeout=1)
        else:
            x = requests.get(STRING_URL + f'/{op}?a={a}&b={b}', timeout=1)
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

@app.route('/log/count/<URL>')
def countLogs(URL):
    try:
        x = requests.get(LOG_URL + f'/countLogs/{URL}', timeout=1)
        x.raise_for_status()
        return x.text
    except ConnectionError:
        return make_response('Log service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

@app.route('/ping/<URL>')
def ping(URL):
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(URL)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise Exception("Invalid URL")
        r = subprocess.run(['/usr/bin/ping', '-w', '2', '-c', '3', URL], capture_output=True) #nosec

        if b"100% packet loss" in r.stdout:
            return make_response('service is down', 404)
        else:
            return make_response(r.stdout, 200)
    except:
        return make_response('error', 500)


def crashLog():
    try:
        x = requests.get(LOG_URL + f'/crash')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Log service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)

def getLogs():
    try:
        x = requests.get(LOG_URL + f'/getLogs')
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('Log service is down\n', 404)
    except HTTPError:
        return make_response('Invalid input\n', 400)