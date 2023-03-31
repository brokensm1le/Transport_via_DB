import curses
import requests
from curses.textpad import Textbox, rectangle
import time
import threading

mutex = threading.Lock()
text = ""
lastRecieved = None
url = None
chatID = None
username = None

def send_message(message):
    global text
    if len(message) == 0:
        return
    r = requests.post(url + "/send", json={"username": username, "chatID": chatID, "message": message})
    if r.status_code != 200:
        raise ValueError("Error sending message. status_code: " + str(r.status_code) + ", text: " + r.text)

def get_messages():
    global text
    global lastRecieved
    while True:
        time.sleep(1)
        mutex.acquire()
        if url is not None and chatID is not None and username is not None:
            r = requests.get(url + "/get", json={"username": username, "chatID": chatID, "lastRecieved": lastRecieved})
            if r.status_code != 200:
                raise ValueError("Error getting messages. status_code: " + str(r.status_code) + ", text: " + r.text)
            js = r.json()
            for message in js:
                text += "[" + message["username"] + "]: " + message["message"] + "\n"
                lastRecieved = message["id"]
        mutex.release()

def get_text(h, w):
    global text
    mutex.acquire()
    messages = text.split("\n")[::-1]
    good = []
    have = 0
    for s in messages:
        have += (len(s) + w - 1) // w
        if have > h:
            break
        good.append(s)
    text = '\n'.join(good[::-1])
    text_ = text
    mutex.release()
    return text_

def main():
    global username
    global url
    global chatID
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    # curses.curs_set(False)
    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    exception = None
    try:
        WindowWidth = curses.COLS
        WindowHeight = curses.LINES
        if WindowHeight < 10:
            raise Exception("Window height must be at least 10")
        if WindowWidth < 10:
            raise Exception("Window width must be at least 10")
        
        WindowInputHeight = max(3, min(10, WindowHeight // 10))
        WindowInputWidth = WindowWidth
        
        WindowOutputHeight = WindowHeight - WindowInputHeight
        WindowOutputWidth = WindowWidth
            
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, get_text(WindowOutputHeight, WindowOutputWidth))

            if url is None:
                stdscr.addstr(WindowOutputHeight, 0, "Enter local_server url: (hit ctrl-G to send)", curses.color_pair(2))
            elif chatID is None:
                stdscr.addstr(WindowOutputHeight, 0, "Enter chatID: (hit ctrl-G to send)", curses.color_pair(2))
            elif username is None:
                stdscr.addstr(WindowOutputHeight, 0, "Enter username: (hit ctrl-G to send)", curses.color_pair(2))
            else:
                stdscr.addstr(WindowOutputHeight, 0, "Enter message: (hit ctrl-G to send) (leave it empty to update history)", curses.color_pair(2))

            rectangle(stdscr, WindowOutputHeight + 1, 0, WindowOutputHeight + 1 + WindowInputHeight - 2, WindowInputWidth - 2)
            winput = curses.newwin(WindowInputHeight - 3, WindowInputWidth - 3, WindowOutputHeight + 2, 1)
            
            stdscr.refresh()
            
            box = Textbox(winput)
            box.edit()
            message = box.gather().strip()

            if url is None:
                url = message
            elif chatID is None:
                chatID = message
            elif username is None:
                username = message
            else:
                send_message(message)
    except Exception as e:
        exception = e

    curses.nocbreak()
    curses.echo()
    # curses.curs_set(True)
    curses.endwin()
    
    if exception is not None:
        raise exception

if __name__ == "__main__":
    receive_thread = threading.Thread(target=get_messages).start()
    main()
    