#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2019/5/3
#     Usage   :
# 下载二进制、直接下载、下载有编码的文本
# 不下载，返回二进制数据，返回文本
import gzip
from time import sleep
from urllib.request import urlopen, Request, ProxyHandler, build_opener

import requests

from src.open.settings import http_proxy, https_proxy

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
proxies = {'http': http_proxy, 'https': https_proxy}


# private

def get_data_requests_proxies(url: str):
    rp = requests.get(url, headers=headers, proxies=proxies)
    if rp.status_code > 399:
        raise Exception(rp.status_code)
    return rp.content


def get_data_requests(url: str):
    # print('start net request')
    rp = requests.get(url, headers=headers,timeout=60)
    # print('requst success')
    return rp.content


def get_data_origin(url: str):
    req = Request(url=url, headers=headers)
    rsb = urlopen(req)
    result = rsb.read()
    return result


def get_data_origin_proxies(url: str):
    proxyHandler = ProxyHandler(proxies)
    opener = build_opener(proxyHandler)
    req = Request(url=url, headers=headers)
    rsb = opener.open(req)
    result = rsb.read()
    return result


funcDict = {True: {True: get_data_requests_proxies, False: get_data_requests},
            False: {True: get_data_origin_proxies, False: get_data_origin}}


def get_func(useRequest: bool, useProxy: bool):
    func = funcDict[useRequest][useProxy]
    return func


def _get_raw_data(url: str, func, time: int = 7):
    for i in range(time):
        try:
            raw_data = func(url)
            return raw_data
        except Exception as e:
            # print_exc()
            sleep(1)
            pass
    raise Exception("无法下载:" + url)


def save_file(data, filename: str):
    with open(filename, 'wb') as file:
        file.write(data)


def save_text_file(data: str, filename: str):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(data)


# public
def get_raw_data(url: str, useRequest: bool = True, useProxy: bool = False) -> bytes:
    func = get_func(useRequest, useProxy)
    return _get_raw_data(url, func)


def get_text(url: str, encodeStr: str, useRequest: bool = True, useProxy: bool = False):
    raw_data = get_raw_data(url, useRequest, useProxy)
    # return raw_data.decode()
    try:
        text = raw_data.decode(encodeStr, errors='ignore')
    except UnicodeDecodeError as e:
        text = gzip.decompress(raw_data).decode(encodeStr)
        # print(text)
    return text


def download_binary_file(url: str, filename: str, useRequest: bool = True, useProxy: bool = False):
    data = get_raw_data(url, useRequest, useProxy)
    save_file(data, filename)


def download_encode_file(url: str, encodeStr: str, filename: str, useRequest: bool = True,
                         useProxy: bool = False):
    data = get_text(url, encodeStr, useRequest, useProxy)
    save_text_file(data, filename)

# def _downLoad(Url):
#     UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
#
#     Connection = "keep-alive"
#     headers = {'User-Agent': UA, 'Connection': Connection}
#     UrlRequest = Request(Url, headers=headers)
#     # text = opener.open(UrlRequest).read()
#     text = urlopen(UrlRequest).read()
#
#     try:
#         text = text.decode('gbk', 'ignore')
#     except UnicodeDecodeError as e:
#         text = gzip.decompress(text).decode('gbk')
#         # print(text)
#     return text
#
#
# def _downLoadByRequest(Url):
#     UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
#     headers = {'User-Agent': UA}
#     r = requests.get(url=Url, headers=headers)
#     r.encoding = 'gbk'
#     return r.text

def main():
    url = ''
    fn = "D:/test.jpg"
    download_binary_file(url, fn, True, True)

    print('Hello world!')


if __name__ == '__main__':
    main()
