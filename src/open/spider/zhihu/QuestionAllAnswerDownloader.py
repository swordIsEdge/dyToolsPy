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
from src.open.spider.zhihu.AnswerParser import parser_page
from src.open.spider.zhihu.ZhihuAnswer import ZhihuAnswer
from traceback import print_exc

PAGE_SIZE = 20


def parserQuestionTitle(jsonStr: str):
    jsonObj = json.loads(jsonStr)
    ques = jsonObj['data'][0]['question']
    title = ques['title']
    url = ques['url']
    titleMark = '# QUESTION  \n\n**' + title + '**  \n' + '[' + title + '](' + url + ')\n\n'
    return titleMark


def downloadQuestionPage(questionId: int, page: int) -> ([ZhihuAnswer], bool, str):
    """
    :param questionId:
    :param page:
    :return: (answerList, hasNextPage)
    """
    offset = page * PAGE_SIZE
    url = f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=content&limit=20&offset={offset}&sort_by=updated'
    # url=f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit=20&offset={offset}&sort_by=updated'
    res = get_text(url, 'utf-8')
    questionTitle = parserQuestionTitle(res)
    ans, hasNext = parser_page(res)
    return ans, hasNext, questionTitle


def downloadQuestion(questionId: int) -> ([ZhihuAnswer], str):
    ssg = RandomSleepSecondGen(2, 18)
    page = 0
    hasNext = True
    answers = []
    questionTitle = None
    while hasNext:
        print(f'download answer of page {page}')
        try:
            page_answers, hasNext, title_ = downloadQuestionPage(questionId, page)
            questionTitle = questionTitle or title_
            answers.extend(page_answers)
        except Exception as e:
            print_exc()
        page += 1
        if hasNext:
            ss = ssg.getNextSleepSecond()
            print(f'sleep for {ss} second')
            sleep(ss)
    return answers, questionTitle


def saveZhihuAnswers(questionId: int, fileDir: str, answers: [ZhihuAnswer], title: str):
    fileName = join(fileDir, 'zhihuAnswers_' + str(questionId) + '.md')
    with open(fileName, 'w', encoding='utf-8') as answerFile:
        answerFile.write(title)
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
    res, title = downloadQuestion(questionId)
    saveZhihuAnswers(questionId, 'D:/zhihu', res, title)


def main():
    ids = [
        1,
        2,
        3
    ]

    for id in ids:
        core(id)
    print('Hello world!')


if __name__ == '__main__':
    main()
