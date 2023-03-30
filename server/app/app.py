from flask import Flask, request
import http
import json
import argparse
import os
import socket

from mongo_worker import mongo_get_messages, mongo_add_message
from utils.signature import SaltSigner

salt_signer = None

app = Flask(__name__)

@app.post('/')
def add_message():
    try:
        data = json.loads(request.data.decode('utf-8'))
        if 'signature' not in data:
            return 'No signature in request\n', http.HTTPStatus.BAD_REQUEST
        if 'chatID' not in data:
            return 'No chatID in request\n', http.HTTPStatus.BAD_REQUEST

        signature = data['signature']
        del data['signature']

        true_signature = hashlib.sha256(salt + json.dumps(data, sort_keys=True)).hexdigest()
        if signature != true_signature:
            return 'Wrong signature\n', http.HTTPStatus.FORBIDDEN
        
        chatID = data['chatID']
        del data['chatID']

        result = mongo_add_message(data, chatID)
        return {'id': result}, http.HTTPStatus.OK        
    except:
        return 'Bad data in request\n', http.HTTPStatus.BAD_REQUEST

@app.get('/')
def get_messages():
    try:
        data = json.loads(request.data.decode('utf-8'))
        if 'chatID' not in data:
            return 'No chatID in request\n', http.HTTPStatus.BAD_REQUEST
        if 'lastRecieved' not in data:
            return 'No lastRecieved in request\n', http.HTTPStatus.BAD_REQUEST
        
        chatID = data['chatID']
        lastRecieved = data['lastRecieved']

        result = mongo_get_messages(lastRecieved, chatID)
        return result, http.HTTPStatus.OK
    except:
        return 'Bad data in request\n', http.HTTPStatus.BAD_REQUEST

if __name__ == '__main__':    
    salt = os.environ.get('SALT')
    salt_signer = SaltSigner(salt=salt)
    print("Salt of signer setted to:", salt_signer.get_salt(), flush=True)
    print("Hosted on:", socket.gethostbyname(socket.gethostname()))

    app.run(host='0.0.0.0', port=5050)
