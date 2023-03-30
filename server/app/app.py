from flask import Flask, request
import http
import json
import hashlib

from mongo_worker import get_messages, add_message

app = Flask(__name__)

@app.post('/')
def add_message():
    try:
        data = json.loads(request.data.decode('utf-8'))
        signature = data['signature']
        del data['signature']
        true_signature = hashlib.sha256(salt + json.dumps(data, sort_keys=True)).hexdigest()
    except:
        return '', http.HTTPStatus.BAD_REQUEST
    