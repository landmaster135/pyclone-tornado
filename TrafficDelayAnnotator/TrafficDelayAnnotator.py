from bs4 import BeautifulSoup as bs4
import urllib.request as ur
import re
import requests

# Read DB
senku_data = open("SENKU_DB.txt", "r")
url_data = open("URL_DB.txt", "r")

# Make DB SENKU List & URL List
SENKU_DB = senku_data.readlines()
URL_DB = url_data.readlines()

# Set Line Notify token and API
line_notify_token = 'INPUT YOUR TOKEN ID'
line_notify_api = 'https://notify-api.line.me/api/notify'

# Import Senku Data and URL from the beginning
for target_senku, url in zip(SENKU_DB, URL_DB):
    req = ur.urlopen(url)
    html = bs4(req, "html.parser")
    match = html.find(class_="corner_block_row_detail_d").string.replace('\n','')
    text = target_senku + '\n ' + match

    # Export only delay or cancel train information by using LINE Notify
    if (match != '現在、平常通り運転しています。' and match != '情報提供時間は4：00～翌2：00となっています。'):
        message = '\n' + text
        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)

# Close DB
senku_data.close()
url_data.close()