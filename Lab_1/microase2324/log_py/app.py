from flask import Flask, request, make_response, jsonify
import redis, threading, time, os

r = redis.Redis(host='db', port=6379, decode_responses=True)

app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'BAD_SECRET_KEY'

@app.route('/getLogs')
def getLogs():
    res = {}
    for key in r.scan_iter(match="*"):
        value = r.get(key)
        res.update({key : value})
    return make_response(jsonify(res), 200)

@app.route('/addLog', methods=['POST'])
def addLog():
    payload = request.json
    key = payload["time"]
    value = payload["log"]
    r.set(key, value)
    return make_response(jsonify('ok'),200)

def create_app():
    return app

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)