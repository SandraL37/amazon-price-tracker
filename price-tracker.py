import requests, json
from bs4 import BeautifulSoup
from os import system, name
from threading import Thread
from time import sleep
import re

def cls():
    system('cls' if name=='nt' else 'clear')

def getprice(link):

    soup = requests.get(link, headers = {
        "referer":"referer: https://www.google.com/",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        })
    soup = BeautifulSoup(soup.text, "html.parser")

    price = soup.find_all("span", id=re.compile("priceblock_.*price"))[0].get_text()

    return [soup.title.string, price]

def threadedprice(LINK, LANG):

    try: print(f"\u001b[38;5;72mamazon\u001b[0m \u001b[38;5;201m{LANG}\u001b[0m \u001b[38;5;72m->\u001b[0m \u001b[32m{getprice(LINK)[1]}\u001b[0m               \u001b[42mlink: {LINK}\u001b[0m\n", end="")
    except: print(f"\u001b[38;5;72mamazon\u001b[0m \u001b[38;5;201m{LANG}\u001b[0m \u001b[38;5;72m->\u001b[0m \u001b[31mnot avabile\u001b[0m               \u001b[41mlink: {LINK}\u001b[0m\n", end="")
    waiter.append(True)

cls()

with open('components.json', 'r') as f: links = json.load(f)

global waiter
while True:
    for COMPONENT, ATTR in links.items():
        print(f"\u001b[33m{COMPONENT} :\u001b[0m\n", end="")

        waiter = []
        for LANG in ATTR["LANG"]:
            Thread(
                target = threadedprice,
                args = [ "https://www.amazon."+LANG+"/dp/"+ATTR["ID"]+"/", LANG ]
            ).start()
        
        while len(waiter) != len(ATTR["LANG"]): sleep(0.1)
        print("\n", end="")
    sleep(600)
