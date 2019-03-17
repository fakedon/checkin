# -*- coding: utf8 -*-

import os
import re
import requests
import time


hostloc_username = os.getenv('hostloc_username')
hostloc_password = os.getenv('hostloc_password')


def start():
    s = requests.session()
    username = hostloc_username
    password = hostloc_password
    login_url = 'https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    s.post(login_url, {"username": username, 'password': password})

    user_info = s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit').text
    current_money = re.search(r'金钱: </em>(\d+).+?</li>', user_info).group(1)
    print("用户%s,你的金钱为%s" % (username, current_money))

    for i in range(20359, 20370):
        s.get('https://www.hostloc.com/space-uid-%s.html' % i)
        time.sleep(3)

    new_money = s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit').text
    new_money = re.search(r'金钱: </em>(\d+).+?</li>', new_money).group(1)

    return "用户%s,你的金钱为%s, %s" % (username, current_money, new_money)


def main_handler(event, context):
    return start()


if __name__ == '__main__':
    start()
