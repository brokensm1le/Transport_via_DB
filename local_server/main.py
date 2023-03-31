import http, requests, os
from flask import Flask, request
from utils.cipher import Cipher
from utils.signature import SaltSigner

salt = os.environ.get('SALT')
salt_signer = SaltSigner(salt=salt)
pub_cipher = Cipher(os.environ.get('PUB_KEY'))
prv_cipher = Cipher(os.environ.get('PRV_KEY'))
address_server = os.environ.get('ADDR_SERVER')

app = Flask(__name__)


@app.post("/send")
def send():
    if request.data:
        try:
            data = request.json
            data['message'] = pub_cipher.encrypt(data['message'])
            data["signature"] = salt_signer.generate_signature(data)
            response = requests.post(address_server, json=data)
        except Exception as e:
            print(e)
            return 'Error while processing request\n' + str(e), http.HTTPStatus.BAD_REQUEST
        return response.text, response.status_code
    else:
        return 'No data in request\n', http.HTTPStatus.BAD_REQUEST


@app.get("/get")
def get():
    if request.data:
        try:
            data = request.json
            response = requests.get(address_server, json=data)
            if response.status_code != http.HTTPStatus.OK:
                return response.text, response.status_code
            data_response = response.json()
            for i in range(len(data_response)):
                data_response[i]["message"] = prv_cipher.decrypt(data_response[i]["message"])
            return data_response, response.status_code
        except Exception as e:
            print(e)
            return 'Error while processing request\n' + str(e), http.HTTPStatus.BAD_REQUEST
    else:
        return  'No data in request\n', http.HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

