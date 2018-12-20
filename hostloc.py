#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
from urllib import request
from http import cookiejar

account_dict = {}
envs = dict(os.environ)
for key, value in envs.items():
    if key.startswith('hostloc_username_'):
        id = key.split('hostloc_username_')[-1]
        password = os.getenv('hostloc_password_' + id)
        if password:
            account_dict[id] = {'username': value, 'password': password}

# account_dict = {
#     '0': {'username': 'xxxx', 'password': 'xxx'},
#     '1': {'username': 'yyyy', 'password': 'xxx'},
#     '2': {'username': 'zzzz', 'password': 'xxx'},
# }


def Login(URL, UserData):
    __cookies = ''
    __cookie = cookiejar.CookieJar()
    __handler = request.HTTPCookieProcessor(__cookie)
    __req = request.Request(URL, data=str(UserData).encode('utf-8'))
    request.build_opener(__handler).open(__req)
    for cookie in __cookie:
        __cookies += cookie.name + '=' + cookie.value + ';'
    return __cookies


def GetPage(URL, Header_Cookies):
    __Header = {'Cookie': str(Header_Cookies)}
    __req = request.Request(URL, headers=__Header)
    return request.urlopen(__req).read().decode('utf-8')


def GetCredit(username, password):
    Login_URL = 'https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    My_Home = 'https://www.hostloc.com/home.php?mod=spacecp&inajax=1'

    user_data = 'username=' + str(username) + '&' + 'password=' + str(password)
    My_Cookies = Login(Login_URL, user_data)

    if '<td>' + str(username) + '</td>' not in GetPage(My_Home, My_Cookies):
        isLogin = False
        print('[%s] Login Fail!' % username)
    else:
        isLogin = True
        print('[%s] Login Success!' % username)

    if isLogin:
        for __x in range(25297, 25309):
            __url = 'https://www.hostloc.com/space-uid-{}.html'.format(__x)
            GetPage(__url, My_Cookies)

def start():
    for account in account_dict.values():
        GetCredit(acount['username'], account['password'])
        time.sleep(5)

if __name__ == '__main__':
    start()
#     for __i in range(0, len(account_dict)):
#         GetCredit(account_dict[str(__i)]['username'], account_dict[str(__i)]['password'])
