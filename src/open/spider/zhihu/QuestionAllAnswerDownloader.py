#!/usr/bin/python
# -*- coding:utf-8 -*-
#     Author  :  kasumi
#     Date    :  2021/5/3 10:21
#     Usage   :
from time import sleep

from src.open.netTools.NetUtils import get_text
from src.open.spider.zhihu.AnswerParser import parser_page
from src.open.spider.zhihu.ZhihuAnswer import ZhihuAnswer

PAGE_SIZE = 20


def downloadQuestionPage(questionId: int, page: int) -> ([ZhihuAnswer], bool):
    """
    :param questionId:
    :param page:
    :return: (answerList, hasNextPage)
    """
    offset = page * PAGE_SIZE
    url=f'https://www.zhihu.com/api/v4/questions/{questionId}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit=20&offset={offset}&sort_by=updated'
    res = get_text(url, 'utf-8')
    return parser_page(res)


def downloadQuestion(questionId: int) -> [ZhihuAnswer]:
    page = 0
    hasNext = True
    answers = []
    while hasNext:
        page_answers, hasNext = downloadQuestionPage(questionId, page)
        page += 1
        answers.extend(page_answers)
        sleep(1)
    return answers


def main():
    questionId = 123456789
    res = downloadQuestion(questionId)
    lines = []
    for re in res:
        line = re.content + '\n\n'
        lines.append(line)
    with open('D:/ans.md', 'w', encoding='utf-8') as zhiansFile:
        zhiansFile.writelines(lines)
    print('Hello world!')


if __name__ == '__main__':
    main()
