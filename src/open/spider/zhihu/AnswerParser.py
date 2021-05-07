#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2021/5/3 10:20
#     Usage   :
from src.open.spider.zhihu.ZhihuAnswer import ZhihuAnswer
import json
import html2text


def parser_single(ans)->ZhihuAnswer:
    try:
        ansId = ans['id']
        authorName = ans['author']['name']
        htmlContent = ans['content']
        markContent = html2text.html2text(htmlContent)
        content = '**作者： ' + authorName + '**  \n\n**内容：**  \n\n' + markContent + '\n\n----\n'
        return ZhihuAnswer(ansId, content)
    except Exception as e:
        ansId = 0
        content = e.__str__()
        return ZhihuAnswer(ansId, content)


def parser_page(pageJsonStr: str) -> ([ZhihuAnswer], bool):
    result = json.loads(pageJsonStr)
    ansList = result['data']
    zhiAnswerList = []
    for ans in ansList:
        zhiAnswer = parser_single(ans)
        zhiAnswerList.append(zhiAnswer)
    isEnd = result['paging']['is_end']
    return zhiAnswerList, not isEnd


def main():
    print('Hello world!')


if __name__ == '__main__':
    main()
