import http, requests, os, hashlib
from flask import Flask, request
import json
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from utils.signature import SaltSigner
from base64 import b64decode, b64encode

salt = os.environ.get('SALT')
salt_signer = SaltSigner(salt=salt)
pub_key = RSA.import_key(b64decode(os.environ.get('PATH_PUB_KEY').encode('utf-8')))
pub_cipher = PKCS1_OAEP.new(pub_key)
prv_key = RSA.import_key(b64decode(os.environ.get('PATH_PRV_KEY').encode('utf-8')))
prv_cipher = PKCS1_OAEP.new(prv_key)
address_server = os.environ.get('ADDR_SERVER')

app = Flask(__name__)


@app.post("/send")
def send():
    print(request.data, flush=True)
    if request.data:
        try:
            data = json.loads(request.data.decode(encoding='utf-8'))
            print(data, flush=True)
            print(pub_key, flush=True)
            data['message'] = b64encode(pub_cipher.encrypt(data['message'].encode('utf-8'))).decode('utf-8')
            print(data, flush=True)
            data["signature"] = salt_signer.generate_signature(data)
            print(data, flush=True)
            response = requests.post(address_server, json=data)
            print(response, flush=True)
        except Exception as e:
            print(e)
            return 'Error while processing request\n' + str(e), http.HTTPStatus.BAD_REQUEST
        return response.json(), response.status_code
    else:
        return 'No data in request\n', http.HTTPStatus.BAD_REQUEST


@app.get("/get")
def get():
    if request.data:
        try:
            data = json.loads(request.data.decode(encoding='utf-8'))

            response = requests.get(address_server, json=data)
            data_response = json.loads(response.text)

            for i in range(len(data_response["messages"])):
                data_response["messages"][i]["message"] = prv_cipher.decrypt(b64decode(data_response["messages"][i]["message"].encode('utf-8'))).decode('utf-8')
        except Exception as e:
            print(e)
            return 'Error while processing request\n' + str(e), http.HTTPStatus.BAD_REQUEST
        return data_response, response.status_code
    else:
        return  'No data in request\n', http.HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

