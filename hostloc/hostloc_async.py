import aiohttp
import asyncio

import argparse
import configparser
import logging
import os
import re
from random import randint


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


async def get_ip(url=None, proxy=None):
    if url is None:
        url = 'https://api.ipify.org'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy) as resp:
            return await resp.text()


accounts = {}
config_file = args.config
if config_file and os.path.isfile(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8-sig")
    for sec in config.sections():
        username = config.get(sec, 'username', fallback=None)
        password = config.get(sec, 'password', fallback=None)
        proxy = {}
        http_proxy = config.get(sec, 'http_proxy', fallback=None)
        https_proxy = config.get(sec, 'https_proxy', fallback=None)
        if username and password:
            if http_proxy:
                proxy['http'] = http_proxy
                if https_proxy:
                    proxy['https'] = https_proxy
                else:
                    proxy['https'] = http_proxy
            else:
                if https_proxy:
                    proxy['https'] = https_proxy
                    proxy['http'] = https_proxy

            _account = {
                'username': username,
                'password': password,
            }
            if proxy:
                _account['proxy'] = proxy
            accounts[username] = _account


envs = dict(os.environ)
for key, value in envs.items():
    if key.startswith('hostloc_username_'):
        env_id = key.split('hostloc_username_')[-1]
        password = os.getenv('hostloc_password_' + env_id)
        proxy = {}
        http_proxy = os.getenv('hostloc_http_' + env_id)
        https_proxy = os.getenv('hostloc_https_' + env_id)
        if password:
            if http_proxy:
                proxy['http'] = http_proxy
                if https_proxy:
                    proxy['https'] = https_proxy
                else:
                    proxy['https'] = http_proxy
            else:
                if https_proxy:
                    proxy['https'] = https_proxy
                    proxy['http'] = https_proxy

            _account = {
                'env_id': env_id,
                'username': value,
                'password': password,
            }
            if proxy:
                _account['proxy'] = proxy
            accounts[value] = _account


async def hostloc_checkin(account):
    username = account.get('username')
    password = account.get('password')
    proxy = account.get('proxy')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    async with aiohttp.ClientSession(headers=headers) as s:
        logger.info('用户: %s, 使用IP: %s', username, await get_ip(proxy=proxy))
        login_url = 'https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        async with s.post(login_url, data={'username': username, 'password': password}, proxy=proxy) as login_post:
            _aes = re.search(r'toNumbers\((\"\w{32}\")\).*toNumbers\((\"\w{32}\")\).*toNumbers\((\"\w{32}\")\)', await login_post.text(), flags=re.S)
        if _aes:
            logger.info("发现防ddos")
            aes_url = 'https://donjs.herokuapp.com/aes/{a}/{b}/{c}'.format(a=_aes.group(1), b=_aes.group(2), c=_aes.group(3))
            async with s.get(aes_url, proxy=proxy) as L7FW:
                L7FW = await L7FW.text()
            login_post.cookies['L7FW'] = L7FW
            login_post_with_cookies = await s.post(login_url, data={'username': username, 'password': password}, proxy=proxy, cookies=login_post.cookies)

        await asyncio.sleep(randint(1, 5))
        async with s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit', proxy=proxy) as user_info:
            user_info = await user_info.text()
        info_pattern = re.compile(r'>用户组: (\w+)</a>.*<em> 金钱: </em>(\d+)  &nbsp; </li>.*<li><em> 威望: </em>(\d+) </li>.*<li class=\"cl\"><em>积分: </em>(\d+) <span', flags=re.S)
        _current = re.search(info_pattern, user_info)
        if _current:
            logger.info("用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _current.group(1), _current.group(2), _current.group(3), _current.group(4))
        else:
            logger.info("用户: %s, 登陆出错", username)
            return
        await asyncio.sleep(randint(1, 5))

        _visit = 0
        visited_space_uids = []
        random_visits = 10 + randint(0, 5)
        while True:
            if _visit == random_visits:
                break
            space_uid = randint(1, 35550)
            if space_uid in visited_space_uids:
                continue
            async with s.get('https://www.hostloc.com/space-uid-%s.html' % space_uid, proxy=proxy) as space_text:
                space_text = await space_text.text()
            visited_space_uids.append(space_uid)
            await asyncio.sleep(randint(1, 5))
            if '抱歉，您指定的用户空间不存在' in space_text:
                logger.debug('用户: %s, 访问UID: %s，不存在', username, space_uid)
                continue
            logger.debug('用户: %s, 访问UID: %s, 成功', username, space_uid)
            _visit += 1
        async with s.get('https://www.hostloc.com/home.php?mod=spacecp&ac=credit', proxy=proxy) as new_user_info:
            new_user_info = await new_user_info.text()
        _new = re.search(info_pattern, new_user_info)
        logger.info("(之前)用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _current.group(1), _current.group(2), _current.group(3), _current.group(4))
        logger.info("(现在)用户: %s, 用户组: %s, 金钱: %s, 威望: %s, 积分: %s", username, _new.group(1), _new.group(2), _new.group(3), _new.group(4))


def start(log_to_file=True):
    if log_to_file:
        fh = logging.FileHandler('hostloc.log', mode='a')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    loop = asyncio.get_event_loop()
    tasks = []
    async def _local_ip():
        logger.debug('本机IP: %s', await get_ip())
    tasks.append(_local_ip())
    for account in accounts.values():
        try:
            tasks.append(hostloc_checkin(account))
        except Exception as e:
            logger.exception(e)
    loop.run_until_complete(asyncio.wait(tasks))
    logger.info('========= 今日任务完成 ==========')


def main_handler(event, context):
    start(interval=60, log_to_file=False)


if __name__ == '__main__':
    start()
