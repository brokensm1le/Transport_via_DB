import time
import requests

from threading import Thread

local_server_port = int(input("Local server port: "))
username = input("Your username: ")
chat_id = input("Chat ID: ")

get_url = f"http://localhost:{local_server_port}/get"
send_url = f"http://localhost:{local_server_port}/send"

def listener():
    last_recieved_message = None
    while True:
        t_start = time.time()

        json_data = {"chatID": chat_id}
        if last_recieved_message is not None:
            json_data["lastRecieved"] = last_recieved_message

        new_messages = requests.get(get_url, json=json_data).json()

        for message in new_messages:
            last_recieved_message = message['id']
            print(f"  {message['username']}:\n{message['message']}\n")

        t_end = time.time()
        if t_end > t_start + 0.2:
            time.sleep(t_end - t_start - 0.2)

Thread(target=listener).start()

while True:
    message = input()
    json_data = {"chatID": chat_id, "username": username, "message": message}
    requests.post(send_url, json=json_data)
