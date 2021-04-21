from queue import Queue
from threading import Thread
import requests
import colorama
from config import threads, attempts

c = colorama.Fore
q = Queue(maxsize=0)
num_threads = (threads)
recheck = int(attempts)

def check(token):
    headers={
            'Authorization': token
        }

    src = requests.get('https://discordapp.com/api/v6/auth/login', headers=headers)

    try:
        if src.status_code == 200:
            with open("valid.txt") as file:
                content = file.read()
                if str(token) in content:
                    file.close()
                    pass
                else:
                    w = open("valid.txt", "a")
                    w.write(f"{token}\n")
                    w.close()
            print(f"{c.LIGHTBLACK_EX}[{c.GREEN}+{c.LIGHTBLACK_EX}] {c.WHITE}token works{c.LIGHTBLACK_EX}! ({c.LIGHTGREEN_EX}{token}{c.LIGHTBLACK_EX}){c.RESET}")
        else:
            print(f"{c.LIGHTBLACK_EX}[{c.RED}-{c.LIGHTBLACK_EX}] {c.WHITE}token does not work{c.LIGHTBLACK_EX}! ({c.LIGHTRED_EX}{token}{c.LIGHTBLACK_EX}){c.RESET}")
            for i in range(recheck):
                try:
                    rechecking = requests.get('https://discordapp.com/api/v6/auth/login', headers=headers)
                    if rechecking.status_code == 200:
                        with open("valid.txt") as file:
                            content = file.read()
                            if str(token) in content:
                                file.close()
                                pass
                            else:
                                w = open("valid.txt", "a")
                                w.write(f"{token}\n")
                                w.close()
                        print(f"{c.LIGHTBLACK_EX}[{c.GREEN}+{c.LIGHTBLACK_EX}] {c.WHITE}token works{c.LIGHTBLACK_EX}! ({c.LIGHTGREEN_EX}{token}{c.LIGHTBLACK_EX}){c.RESET}")
                        break
                    else:
                        print(f"{c.LIGHTBLACK_EX}[{c.YELLOW}?{c.LIGHTBLACK_EX}] {c.WHITE}rechecking token{c.LIGHTBLACK_EX}! ({c.LIGHTYELLOW_EX}{token}{c.LIGHTBLACK_EX}){c.RESET}")
                except:
                    print("Yeah we can't contact discordapp.com")
    except Exception:
        print("Yeah we can't contact discordapp.com")

def run(q):
    while True:
        check(q.get())
        q.task_done()

for i in range(num_threads):
    worker = Thread(target=run, args=(q,))
    worker.setDaemon(True)
    worker.start()

f = open("tokens.txt", "r")
tokens = f.readlines()
for token in tokens:
    q.put(token.strip())

q.join()
