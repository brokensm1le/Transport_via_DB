# Transport_via_DB

## LocalServer

Пострелять Curl-ом:
```
curl -XPOST http://localhost:8080/send -H 'accept: application/json' -H 'Content-Type: application/json' 
-d '{"chatID":"kek1", "message": "hello", "username": "vasya"}'
```
Через Python:
```
import requests

data = {'chatID': 'kek1',
        'message': "hello world",
        'username': "vasya"}

response = requests.post('http://localhost:8080/send', json=data)
print(response)
```
