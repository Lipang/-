#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: daning
import time
import re
import requests
import execjs


def get_sign_func():
    with open('./sign.js', 'r', encoding='utf-8') as f:
        c = execjs.compile(f.read())
    return c


def get_token_and_gtk():
    url = 'https://fanyi.baidu.com/'
    headers = {
        'Host': 'fanyi.baidu.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie': user_cookie
    }
    html = requests.get(url, headers=headers)
    gtk = re.findall("window.gtk = '(.*?)';", html.text, re.S)[0]
    token = re.findall("window\\['common'].*token: '(.*?)',.*?systime", html.text, re.S)[0]
    if gtk and token:
        return gtk, token
    else:
        print("没找到")


def trans(query, token, sign):
    trans_url = 'https://fanyi.baidu.com/v2transapi'
    formdata = {
        'from': 'zh',
        'to': 'en',
        'query': query,
        'transtype': 'enter',
        'simple_means_flag': '3',
        'sign': sign,
        'token': token  # 这里的token和cookie有对应关系，可以换成你自己的
    }
    headers = {
        'Host': 'fanyi.baidu.com',
        'Origin': 'https://fanyi.baidu.com',
        'Pragma': 'no-cache',
        'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': user_cookie
    }
    response = requests.post(trans_url, headers=headers, data=formdata)
    try:
        response = response.json()
        result = response['trans_result']['data'][0]['result'][0][1]
        print(f'“{query}” 的翻译结果: {result}\n')
    except KeyError:
        raise KeyError('出错了')


if __name__ == '__main__':
    user_cookie = input('请输入你的cookie: ')
    gtk, token = get_token_and_gtk()
    get_sign = get_sign_func()
    while True:
        trans_str = input("请输入要翻译的文本: ")
        sign = get_sign.call('hash', trans_str, gtk)
        s_time = time.time()
        trans(trans_str, token, sign)
