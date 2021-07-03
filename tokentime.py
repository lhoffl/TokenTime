import requests
import sys
import os
import json
import datetime
import http.client
import time
import math
from dateutil import parser
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
from pathlib import Path

def send(message):

    webhookurl = "WEBHOOK"

    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"

    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })

    response = connection.getresponse()
    result = response.read()

    return result.decode("utf-8")


lockFile = '/home/minecraftin/tokentime/token.lock'
GAMES_PLAYED_TODAY = path.exists(lockFile)

encoreLockFile = '/home/minecraftin/tokentime/encore.lock'
ENCORE_TODAY = path.exists(encoreLockFile)

if(ENCORE_TODAY and GAMES_PLAYED_TODAY):
    quit()

url = 'https://overwatchleague.com/en-us/schedule'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
data = json.loads(soup.select("[type='application/json']")[0].string)
matches = data['props']['pageProps']['blocks'][2]['schedule']['tableData']['events'][0]['matches']

for match in matches:
    if match['venue']['title'] != "East":

        startDate = math.floor(match['startDate'] / 1000) - 1800
        currentDate = math.floor(time.time())

        if currentDate >= startDate and match['status'] != "CONCLUDED":

            matchInfo = match['competitors'][0]['name'] + " vs " + match['competitors'][1]['name']
            print(matchInfo + " is the current game")

            if not GAMES_PLAYED_TODAY and not match['isEncore']:
                Path(lockFile).touch()
                send("Kick it Simon, it's Token Time! <:outlawsBestTeam:603620338521211082> <@&779183041368555560> <:outlawsBestTeam:603620338521211082> https://overwatchleague.com/en-us/" + matchInfo + " is the first game of the day")
            elif not ENCORE_TODAY and match['isEncore']:
                Path(encoreLockFile).touch()
                send("Kick it Simon, it's Encore Time! <:outlawsBestTeam:603620338521211082> <@&784536328481406998> <:outlawsBestTeam:603620338521211082> https://overwatchleague.com/en-us/" + matchInfo + " is the first encore game")
