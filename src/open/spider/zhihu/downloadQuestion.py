#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2021/5/3 10:21
#     Usage   :
import json
from os.path import join
from time import sleep

from src.open.netTools.NetUtils import get_text
from src.open.randomTools.randomGen import RandomSleepSecondGen
from src.open.spider.zhihu.answerParser import parser_page
from src.open.spider.zhihu.ZhihuAnswer import ZhihuAnswer
from traceback import print_exc

PAGE_SIZE = 20

questionTitle = ''
questionUrl = ''


def parserQuestionTitle(jsonStr: str):
    jsonObj = json.loads(jsonStr)
    ques = jsonObj['data'][0]['question']
    global questionTitle, questionUrl
    questionTitle = ques['title']
    questionUrl = ques['url']
    print('download question ' + questionTitle)


def downloadQuestionPage(questionId: int, page: int) -> ([ZhihuAnswer], bool):
    """
    :param questionId:
    :param page:
    :return: (answerList, hasNextPage)
    """
    offset = page * PAGE_SIZE
    url = f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=content&limit={PAGE_SIZE}&offset={offset}&sort_by=updated'
    # url=f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit={PAGE_SIZE}&offset={offset}&sort_by=updated'
    res = get_text(url, 'utf-8')
    if page == 0:
        parserQuestionTitle(res)
    ans, hasNext = parser_page(res)
    return ans, hasNext


def downloadQuestion(questionId: int) -> ([ZhihuAnswer]):
    ssg = RandomSleepSecondGen(8, 20,4)
    page = 0
    hasNext = True
    answers = []
    while hasNext:
        print(f'download answer of page {page}')
        try:
            page_answers, hasNext = downloadQuestionPage(questionId, page)
            answers.extend(page_answers)
        except Exception as e:
            print_exc()
        page += 1
        if hasNext:
            ss = ssg.getNextSleepSecond()
            print(f'sleep for {ss} second')
            sleep(ss)
    return answers


def saveZhihuAnswers(questionId: int, fileDir: str, answers: [ZhihuAnswer]):
    fileName = join(fileDir, 'zhihuAnswers_' + str(questionId) + '.md')
    global questionTitle, questionUrl
    titleMd = '# QUESTION  \n\n**' + questionTitle + '**  \n' + '[' + questionTitle + '](' + questionUrl + ')\n\n'

    with open(fileName, 'w', encoding='utf-8') as answerFile:
        answerFile.write(titleMd)
        answerFile.write('\n')

        for i, answer in enumerate(answers):
            if i % 10 == 0:
                title = '# PAGE ' + str(i // 10) + ' \n\n'
                answerFile.write(title)
            title2 = '## ANSWER ' + str(i) + '\n\n'
            answerFile.write(title2)
            line = answer.content + '\n\n'
            answerFile.write(line)


def core(questionId: int):
    res = downloadQuestion(questionId)
    saveZhihuAnswers(questionId, 'D:/zhihu', res)


def main():
    questionIdList = [
        37005979

                      ]
    for qId in questionIdList:
        core(qId)
    print('Hello world!')


if __name__ == '__main__':
    main()
