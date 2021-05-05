#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2021/5/3 10:21
#     Usage   :
from src.open.netTools.NetUtils import get_text


def downloadQuestion(questionId:int):
    url= f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?offset=0&limit=20&sort_by=updated'
    res = get_text(url,'utf-8')
    return res

def main():
    questionId = 412028518
    res = downloadQuestion(questionId)
    print(res)
    print('Hello world!')


if __name__ == '__main__':
    main()
