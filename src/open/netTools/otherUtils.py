#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2019/5/3
#     Usage   :
from os.path import split
from random import randint

from src.privatecode.commonTools.randomTools import randomString


def get_filename_from_url(url: str) -> str:
    origin = split(url)[-1]
    if origin:
        if '?' in origin and not origin.startswith('?'):
            ri = origin.index('?')
            origin = origin[:ri]

        elif '#' in origin and not origin.startswith('#'):
            ri = origin.index('#')
            origin = origin[:ri]

    return origin if origin else 'random' + randomString(5)


def get_random_filename_from_url(url: str) -> str:
    original_name = get_filename_from_url(url)
    if '.' in original_name:
        dot_index = original_name.rindex('.')
        ri = randint(0, 1024)
        new_name = original_name[0:dot_index] + 'random' + str(ri) + '.' + original_name[dot_index + 1:]
        return new_name
    else:
        return randomString(5) + original_name


def main():
    url = 'https://alimov2.a.yximgs.com/upic/2020/06/22/19/BMjAyMDA2MjIxOTAxMjFfNTg1MTc0MDY4XzMwOTc2NDQwMzQzXzJfMw==_b_B8a12ce248651329a8772608d253ae7da.mp4'
    print(get_filename_from_url(url))


if __name__ == '__main__':
    main()
