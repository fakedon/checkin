#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from urllib import request
from http import cookiejar

hostloc_username = os.getenv('hostloc_username')
hostloc_password = os.getenv('hostloc_password')

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
    GetCredit(hostloc_username, hostloc_password)

if __name__ == '__main__':
    GetCredit(hostloc_username, hostloc_password)
