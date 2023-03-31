# Транспорт поверх MongoDB

## Постановка задачи:
Данный проект реализует транспорт сообщений для мессенджера (клиент-клиент) описанный в [ideas.md#C](https://github.com/decentralized-hse/Cirriculum/blob/main/ideas.md#c-%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80-%D0%BC%D0%B5%D1%81%D1%81%D0%B5%D0%BD%D0%B4%D0%B6%D0%B5%D1%80%D1%8B-%D0%B8-%D1%87%D0%B0%D1%82%D1%8B).

## Реализация

Транспорт поверх MongoDB будет реализован посредствам коммуникации с заменяемым прокси-сервером, хранящим сообщения в MongoDB. Сообщения хранятся в зашифрованном виде. В одной базе можно хранить несколько чатов, имеющих произвольные ```chatID```.

Каждый клиент транспорта должен запустить локальный сервер с соответствующими ключами (соль для подписи, приватный и публичный ключи для шифрования). Локальный сервер инкапсулирует шифрование и подпись сообщений, а также отправляет их на прокси-сервер для хранения. Также локальный сервер может получать сообщения с прокси-сервера. 

Заметим, что сообщения упорядочены по id, то есть бОльший соответствует более позднему сообщению.

Также заметим, что необходимыми полями в сообщении являются только текст сообщения ```message```, идентификатор чата ```chatID``` и имя пользователя ```username```. К этому набору можно добалять любые другие необходимые поля, например ```parentID```.

## Прокси сервер

Запустить с тестовыми ключами:
```
make run_server \
  SALT=ZGmECFHIly \
  ME_USER=user \
  ME_PASSWORD=userIsAbobus
```

Пользоваться API прокси напрямую не следует, так как первым делом прокси проверяет подпись и данные в MongaDB лежат зашифрованные. Но мы все же попробуем.

Допустим, злоумышленник узнал ip адрес нашего прокси-сервера, прослушиваемый порт и его API и хочет послать сообщение. 

Без подписи сообщения он получит код ответа 400 (BAD REQUEST):
```
curl --request POST \                                                                                                                                       
  --url http://51.250.96.131:5050/ \
  --header 'Content-Type: application/json' \
  --data '{
        "chatID": "skynet",
        "message": "Hello there",
        "username": "IAmTheOneWhoKnocks"
}'
No signature in request
```

С неверной подписью сообщения он получит код ответа 403 (FORBIDDEN)
```
curl --request POST \
  --url http://51.250.96.131:5050/ \
  --header 'Content-Type: application/json' \
  --data '{
        "chatID": "skynet",
        "message": "Hello there",
        "username": "IAmTheOneWhoKnocks",
        "signature": "Walter White"
}'
Wrong signature
```

Аналогично, если злоумышленник хочет прочитать сообщение, ему потребуется подписать название чата, который он хочет прочитать. 

## Локальный сервер

Запустить с тестовыми ключами на порту 5000
```
make run_local_server \
SALT=ZGmECFHIly \
PATH_PUB_KEY=keys/public_key.pem \
PATH_PRV_KEY=keys/private_key.pem \
ADDR_SERVER=http://51.250.96.131:5050
```

**Отправить сообщение в чат:**
```
curl --request POST \
  --url http://localhost:5000/send \
  --header 'Content-Type: application/json' \
  --header 'accept: application/json' \
  --data '{
        "chatID": "100500",
        "message": "This is horosho",
        "username": "AlexT"
}'
```
Ответ:
```
{"id":"642709d46e36d7c335057bab"}
```

**Прочитать все сообщения чата:**
```
curl --request GET \
  --url http://localhost:5000/get \
  --header 'Content-Type: application/json' \
  --header 'accept: application/json' \
  --data '{
        "chatID": "100500"
}'
```
Ответ:
```
[
  {"id":"642709d46e36d7c335057bab","message":"This is horosho","username":"AlexT"},
  {"id":"64270a8e6e36d7c335057bac","message":"This is really nice!","username":"AlexA"}
]
```

**Прочитать последние сообщения чата:**
```
curl --request GET \
  --url http://localhost:5000/get \
  --header 'Content-Type: application/json' \
  --header 'accept: application/json' \
  --data '{
	"chatID": "100500",
	"lastRecieved": "642709d46e36d7c335057bab"
}'
```
Ответ:
```
[
  {"id":"64270a8e6e36d7c335057bac","message":"This is really nice!","username":"AlexA"}
]
```

## Mongo Express

Для удобства смотреть на данные и управлять ими в MongoDB можно через UI доступный по http://51.250.96.131:8081. Тестовый логин - ```user```. Тестовый пароль - ```userIsAbobus```.


