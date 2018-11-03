# coding: utf-8

import requests
import re
import os

# if you don't have a config.py
# You can set ipt_username, ipt_password yourself

ipt_username = os.getenv('ipt_username')
ipt_password = os.getenv('ipt_password')


def ipt_checkin():
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Referer': 'https://iptorrents.com/login.php',
                'Origin': 'https://iptorrents.com/'
              }
    session = requests.Session()
    session.headers.update(headers)
    
    data = dict(username=ipt_username, password=ipt_password}
    resp = session.post('https://iptorrents.com/take_login.php', data=data)

    print(resp.text)

if __name__ == '__main__':
    ipt_checkin()
