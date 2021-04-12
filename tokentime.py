import requests
import sys
import os
import json
import datetime
import http.client
from dateutil import parser
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
from pathlib import Path

def send(message):

    webhookurl = "WEBHOOK_GOES_HERE"

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

if(GAMES_PLAYED_TODAY):
    quit()

url = 'https://overwatchleague.com/en-us/schedule'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
data = json.loads(soup.select("[type='application/json']")[0].string)
matches = data['props']['pageProps']['blocks'][2]['schedule']['tableData']['events'][0]['matches']

for match in matches:
    if match['venue']['title'] == "West":
        if match['venue']['InProgress'] and not GAMES_PLAYED_TODAY:
            Path(lockFile).touch()
            send("Kick it Simon, it's Token Time! <@ID> https://overwatchleague.com/en-us/")
