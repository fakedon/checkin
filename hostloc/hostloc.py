#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import configparser
import logging
import os
import re
import time
from random import randint

import requests


HOSTLOC_DIR = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(HOSTLOC_DIR, 'hostloc.log')

parser = argparse.ArgumentParser(description='Hostloc auto checkin')
parser.add_argument('-c', '--config', )
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_ip(url=None, proxies=None):
    if url is None:
        url = 'https://api.ipify.org'
    return requests.get(url, proxies=proxies).text


accounts = {}
config_file = args.config
if config_file and os.path.isfile(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    for sec in config.sections():
        username = config.get(sec, 'username', fallback=None)
        password = config.get(sec, 'password', fallback=None)
        proxies = {}
        http_proxy = config.get(sec, 'http_proxy', fallback=None)
        https_proxy = config.get(sec, 'https_proxy', fallback=None)
        if username and password:
            if http_proxy:
                proxies['http'] = http_proxy
                if https_proxy:
                    proxies['https'] = https_proxy
                else:
                    proxies['https'] = http_proxy
            else:
                if https_proxy:
                    proxies['https'] = https_proxy
                    proxies['http'] = https_proxy

            _account = {
                'username': username,
                'password': password,
            }
            if proxies:
                _account['proxies'] = proxies
            accounts[username] = _account


envs = dict(os.environ)
for key, value in envs.items():
    if key.startswith('hostloc_username_'):
        env_id = key.split('hostloc_username_')[-1]
        password = os.getenv('hostloc_password_' + env_id)
        proxies = {}
        http_proxy = os.getenv('hostloc_http_' + env_id)
        https_proxy = os.getenv('hostloc_https_' + env_id)
        if password:
            if http_proxy:
                proxies['http'] = http_proxy
                if https_proxy:
                    proxies['https'] = https_proxy
                else:
                    proxies['https'] = http_proxy
            else:
                if https_proxy:
                    proxies['https'] = https_proxy
                    proxies['http'] = https_proxy

            _account = {
                'env_id': env_id,
                'username': value,
                'password': password,
            }
            if proxies:
                _account['proxies'] = proxies
            accounts[value] = _account


def hostloc_checkin(account):
    username = account.get('username')
    password = account.get('password')
    proxies = account.get('proxies')
    s = requests.session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    s.headers.update(headers)
    logger.info('使用IP: {}'.format(get_ip(proxies=proxies)))
    login_url = 'https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
    s.post(login_url, {'username': username, 'password': password}, proxies=proxies)
    time.sleep(randint(1, 5))
    user_info = s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit', proxies=proxies).text
    info_pattern = re.compile(r'>用户组: (\w+)</a>.*<em> 金钱: </em>(\d+)  &nbsp; </li>.*<li><em> 威望: </em>(\d+) </li>.*<li class=\"cl\"><em>积分: </em>(\d+) <span', flags=re.S)
    _current = re.search(info_pattern, user_info)
    if _current:
        logger.info("用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _current.group(1), _current.group(2), _current.group(3), _current.group(4))
    else:
        logger.info("登陆出错")
        return
    time.sleep(randint(1, 5))

    _visit = 0
    visited_space_uids = []
    random_visits = 10 + randint(0, 5)
    while True:
        if _visit == random_visits:
            break
        space_uid = randint(1, 35550)
        if space_uid in visited_space_uids:
            continue
        space_text = s.get('https://www.hostloc.com/space-uid-%s.html' % space_uid, proxies=proxies).text
        visited_space_uids.append(space_uid)
        time.sleep(randint(1, 5))
        if '抱歉，您指定的用户空间不存在' in space_text:
            logger.debug('访问UID: %s，不存在', space_uid)
            continue
        logger.debug('访问UID: %s, 成功', space_uid)
        _visit += 1
    new_user_info = s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit', proxies=proxies).text
    _new = re.search(info_pattern, new_user_info)
    logger.info("(之前)用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _current.group(1), _current.group(2), _current.group(3), _current.group(4))
    logger.info("用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _new.group(1), _new.group(2), _new.group(3), _new.group(4))


def start(interval=None, log_to_file=True):
    if log_to_file:
        fh = logging.FileHandler('hostloc.log', mode='a')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    logger.debug('本机IP: %s', get_ip())
    _first = True
    _wait_time = interval or 3 * 60
    for account in accounts.values():
        if not _first:
            logger.debug('等待%s分钟处理下一个任务', _wait_time // 60)
            time.sleep(int(_wait_time))
        _first = False
        try:
            hostloc_checkin(account)
        except Exception as e:
            logger.exception(e)
    logger.info('========= 今日任务完成 ==========')


def main_handler(event, context):
    return start(interval=60, log_to_file=False)


if __name__ == '__main__':
    start()
