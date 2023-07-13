import requests
import sys
import os
import json
import datetime
import http.client
import time
import math
import syslog
from dateutil import parser
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
from pathlib import Path
from discord_webhook import DiscordWebhook
import urllib.request
import re

teamEmoji = {
    "Vegas Eternal": "<:eternal:1101180161862406144>",
    "Seoul Infernal": "<:Infernal:1101179944622628965>",
    "Seoul Dynasty": "<:dynasty:1101180024121466990>",
    "London Spitfire": "<:spitfire:1101180326425931816>",
    "New York Excelsior": "<:excelsior:1101180316334424204>",
    "Boston Uprising": "<:uprising:1101180230254735515>",
    "Washington Justice": "<:justice:1101180061979246653>",
    "Los Angeles Valiant": "<:valiant:1101180047529889942>",
    "Vancouver Titans": "<:titans:1101180035756466177>",
    "Hangzhou Spark": "<:spark:1101180009638543460>",
    "Atlanta Reign": "<:reign:603620338932121610>",
    "Los Angeles Gladiators": "<:gladiators:603620338919538688>",
    "Guangzhou Charge": "<:charge:603620338814943232>",
    "Toronto Defiant": "<:defiantshill:603620338793709613>",
    "Dallas Fuel": "<:fuel:603620338760286237>",
    "San Francisco Shock": "<:shock:603620338734989333>",
    "Florida Mayhem": "<:mayhem:603620338714148885>",
    "Houston Outlaws": "<:outlawsBestTeam:603620338521211082>",
    "Shanghai Dragons": "<:dragons:603620207482765493>"
}

def send(message):

    webhookurl = "web"

    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"

    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })

    response = connection.getresponse()
    result = response.read()

    return result.decode("utf-8")

syslog.syslog("Simon is looking for games")

lockFile = '/home/fowl/tokenTime/token.lock'
GAMES_PLAYED_TODAY = path.exists(lockFile)

encoreLockFile = '/home/fowl/tokenTime/encore.lock'
ENCORE_TODAY = path.exists(encoreLockFile)

if(ENCORE_TODAY and GAMES_PLAYED_TODAY):
    quit()

url = 'https://overwatchleague.com/en-us/schedule'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
data = json.loads(soup.select("[type='application/json']")[0].string)

print(data)

matches = data['props']['pageProps']['blocks'][2]['schedule']['tableData']['events'][0]['matches']
matches += data['props']['pageProps']['blocks'][2]['schedule']['tableData']['events'][1]['matches']

gamesToday = []

for match in matches:
    startDate = math.floor(match['startDate'] / 1000)
    currentDate = math.floor(time.time())

    if startDate - currentDate >= 0 and currentDate + 69000 >= startDate:
            team1 = match['competitors'][0]['name']
            team2 = match['competitors'][1]['name']

            team1Emoji = ""
            if(teamEmoji.get(team1) != None):
                team1Emoji = teamEmoji[team1]

            team2Emoji = ""
            if(teamEmoji.get(team2) != None):
                team2Emoji = teamEmoji[team2]


            matchInfo =  team1Emoji + " " + team1 + " vs " + team2Emoji + " " + team2
            gamesToday.append(matchInfo)


print(gamesToday)

if(len(gameToday) == 0):
    quit()

for match in matches:

    if match['venue']['title'] != "East Region":

        startDate = math.floor(match['startDate'] / 1000) - 1800
        currentDate = math.floor(time.time())

        if currentDate >= startDate and match['status'] != "CONCLUDED":
            if not GAMES_PLAYED_TODAY and not match['isEncore']:
                Path(lockFile).touch()
                GAMES_PLAYED_TODAY = path.exists(lockFile)

                html = urllib.request.urlopen("https://www.youtube.com/@overwatchleague")
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                video = ("https://www.youtube.com/watch?v=" + video_ids[0])

                schedule = "\n".join(gamesToday)
                webhook = DiscordWebhook(url='web', content= "Kick it Simon, it's Token Time! <@&779183041368555560>\n" + video + "\n" + "Today's schedule is:\n" + schedule +"\n")
                response = webhook.execute()
                syslog.syslog("Simon found the following games: " + schedule)
                syslog.syslog("Simon found the following link: " + video_ids[0])
                quit()
                send("Kick it Simon, it's Token Time! <@&779183041368555560>\nhttps://overwatchleague.com/en-us/\n" + "Today's schedule is:\n" + schedule +"\n")
            elif not ENCORE_TODAY and match['isEncore']:
                Path(encoreLockFile).touch()
                ENCORE_TODAY = path.exists(encoreLockFile)
               # send("Kick it Simon, it's Encore Time! <:outlawsBestTeam:603620338521211082> <@&784536328481406998> <:outlawsBestTeam:603620338521211082> https://overwatchleague.com/en-us/" + matchInfo + " is the first encore game")
