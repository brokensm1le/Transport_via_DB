import http, requests, os, hashlib
from flask import Flask, request
import json
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from utils.signature import SaltSigner

salt = os.environ.get('SALT')
salt, salt_signer = SaltSigner(salt=salt)
path_pub_key = os.environ.get('PATH_PUB_KEY')
path_prv_key = os.environ.get('PATH_PRV_KEY')
address_server = os.environ.get('ADDR_SERVER')

app = Flask(__name__)


@app.route("/send", methods=['POST'])
def send() -> (http.HTTPStatus, requests.Response):
    if request.data:
        try:
            data = json.loads(request.data.decode(encoding='utf-8'))
            print(data)
            key = RSA.import_key(open(path_pub_key).read())
            cipher = PKCS1_OAEP.new(key)
            data['message'] = cipher.encrypt(data['message'])
            data["signature"] = salt_signer.generate_signature(data)

            response = requests.post(address_server, json=data)
        except:
            return http.HTTPStatus.BAD_REQUEST, None
        return response.status_code, response.json()
    else:
        return http.HTTPStatus.BAD_REQUEST, None


@app.route("/get", methods=['GET'])
def get() -> (http.HTTPStatus, requests.Response):
    if request.data:
        try:
            data = json.loads(request.data.decode(encoding='utf-8'))

            response = requests.get(address_server, json=data)
            data_response = json.loads(response.text)

            key = RSA.import_key(open(path_prv_key).read())
            cipher = PKCS1_OAEP.new(key)
            for i in range(len(data_response["messages"])):
                data_response["messages"][i]["message"] = cipher.decrypt(data_response["messages"][i]["message"])
        except:
            return http.HTTPStatus.BAD_REQUEST, None
        return response.status_code, data_response
    else:
        return http.HTTPStatus.BAD_REQUEST, None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

