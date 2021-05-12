#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2021/5/12 22:42
#     Usage   :  有些问题的答案太多了，不得不分批下载，分批存储
import json
from os import makedirs
from os.path import join, exists
import pickle
from time import sleep
from traceback import print_exc

from src.open.netTools.NetUtils import get_text
from src.open.randomTools.randomGen import RandomSleepSecondGen
from src.open.spider.zhihu.answerParser import parser_page
from src.open.spider.zhihu.ZhihuAnswer import ZhihuAnswer

BATCH_PAGE_SIZE = 10
PAGE_SIZE = 20
ROOT_DIR = r'D:/zhihu'
META_FILENAME = 'question_info'


class QuestionInfo:
    def __init__(self):
        self.questionId = 1
        self.info = ''
        self.lastSuccessBatch = -1


def getQuestionRootDir(questionId: int):
    return join(ROOT_DIR, 'batch_' + str(questionId))


def hasInit(questionId: int) -> bool:
    return exists(getQuestionRootDir(questionId))


def getBatchPageNums(batch: int) -> [int]:
    return list(range(BATCH_PAGE_SIZE * batch, BATCH_PAGE_SIZE * (batch + 1)))


def saveQuestionInfo(questionInfo: QuestionInfo):
    qid = questionInfo.questionId
    qrd = getQuestionRootDir(qid)
    qifn = join(qrd, 'question_info_' + str(qid) + '.txt')
    with open(qifn, 'wb')as qif:
        pickle.dump(questionInfo, qif)


def readQuestionInfo(questionId: int) -> QuestionInfo:
    qrd = getQuestionRootDir(questionId)
    qifn = join(qrd, 'question_info_' + str(questionId) + '.txt')
    with open(qifn, 'rb')as qif:
        return pickle.load(qif)


def parserQuestionInfo(questionId: int) -> QuestionInfo:
    url = f"https://www.zhihu.com/api/v4/questions/{questionId}"
    res = get_text(url, 'utf-8')
    questionMap = json.loads(res)
    title = questionMap['title']
    questionInfo = QuestionInfo()
    questionInfo.questionId = questionId
    questionInfo.info = title
    return questionInfo


def initQuestion(questionId: int) -> QuestionInfo:
    print(f'init question {questionId}')
    qrd = getQuestionRootDir(questionId)
    makedirs(qrd)
    questionInfo = parserQuestionInfo(questionId)
    saveQuestionInfo(questionInfo)
    return questionInfo


def saveBatchAnswer(questionId: int, answers: [ZhihuAnswer], batch: int):
    qrd = getQuestionRootDir(questionId)
    fileName = join(qrd, 'answers_batch_' + str(batch) + '.md')
    with open(fileName, 'w', encoding='utf-8') as answerFile:
        answerFile.write('\n')
        for i, answer in enumerate(answers):
            if i % PAGE_SIZE == 0:
                title = '# PAGE ' + str(i // PAGE_SIZE + BATCH_PAGE_SIZE * batch) + ' \n\n'
                answerFile.write(title)
            title2 = '## ANSWER ' + str(i) + '\n\n'
            answerFile.write(title2)
            line = answer.content + '\n\n'
            answerFile.write(line)


def mergeAnswer():
    pass


def downloadQuestionPage(questionId: int, page: int) -> ([ZhihuAnswer], bool):
    """
    :param questionId:
    :param page:
    :return: (answerList, hasNextPage)
    """
    print(f'download page {page}')
    offset = page * PAGE_SIZE
    url = f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=content&limit={PAGE_SIZE}&offset={offset}&sort_by=updated'
    res = get_text(url, 'utf-8')

    ans, hasNext = parser_page(res)
    return ans, hasNext


def downloadOfBatch(batch: int, questionId: int):
    print(f'download batch {batch}')
    ssg = RandomSleepSecondGen(2, 10, 3)

    pages = getBatchPageNums(batch)
    answers = []

    for page in pages:
        hasNext = True
        try:
            ans, hasNext = downloadQuestionPage(questionId, page)
            answers.extend(ans)
        except:
            print_exc()

        if not hasNext:
            break
        else:
            ss = ssg.getNextSleepSecond()
            print(f'sleep for {ss} second')
            sleep(ss)
    saveBatchAnswer(questionId, answers, batch)


def downloadFirstAndInit(questionId: int):
    questionInfo = initQuestion(questionId)
    downloadOfBatch(0, questionId)
    questionInfo.lastSuccessBatch = 0
    saveQuestionInfo(questionInfo)


def downloadBatch(questionId: int):
    questionInfo = readQuestionInfo(questionId)
    batch = questionInfo.lastSuccessBatch
    batch += 1

    downloadOfBatch(batch, questionId)

    questionInfo.lastSuccessBatch = batch
    saveQuestionInfo(questionInfo)


def core(questionId: int):
    if not hasInit(questionId):
        downloadFirstAndInit(questionId)
    else:
        downloadBatch(questionId)


def main():
    questionId = 313210162
    core(questionId)
    print('Hello world!')


if __name__ == '__main__':
    main()
