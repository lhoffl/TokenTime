import requests
import sys
import os
import json
import datetime
import http.client
from dateutil import parser
from bs4 import BeautifulSoup
from datetime import datetime

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

def check_contenders(value) :

    schedule = data['props']['pageProps']['blocks'][2]['tabs']['tabs'][value]

    html = schedule['blocks'][0]['richTextEditor']['articleRawHtml']
    soup = BeautifulSoup(str(html), "lxml")
    dates = soup.find_all('div', attrs={'class': 'schedule-row'})

    now = datetime.now()

    for date in dates:
        d_str = date.find('div', attrs={'class' : 'schedule-date'}).text

        if d_str == "Date":
            continue

        parsed_date = parser.parse(d_str)

        if parsed_date.date() == now.date():
            est = int(date.find('div', attrs={'class' : 'pacific-time'}).text.split(':')[0]) + 3
            current_hour = int(str(now.time()).split(':')[0])
            current_min = int(str(now.time()).split(':')[1])

            if(current_min <= 10 and current_hour == est):
                send("Token time! https://overwatchleague.com/en-us/contenders")

EU_CONTENDERS_ID = 2
NA_CONTENDERS_ID = 4

url = 'https://overwatchleague.com/en-us/contenders/schedule?tab=north_america'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, "lxml")
data = json.loads(soup.select("[type='application/json']")[0].string)

check_contenders(NA_CONTENDERS_ID)
check_contenders(EU_CONTENDERS_ID)
