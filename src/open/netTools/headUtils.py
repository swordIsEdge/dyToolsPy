#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2019/9/13
#     Usage   :
import requests

from src.open.settings import http_proxy, https_proxy

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
proxies = {'http': http_proxy, 'https': https_proxy}



def get_head_requests_proxies(url: str):
    rp = requests.head(url, headers=headers, proxies=proxies)
    return rp


def get_head_requests(url: str):
    rp = requests.head(url, headers=headers)
    return rp


