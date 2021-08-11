#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: DataCollect.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import random
from abc import ABC, abstractmethod
import requests
import re
import logging
from GitActionURL import Ha28ActionUrl


class GitDataCollect(ABC):
    env_token = os.getenv('EXCEL_API_TOKEN')
    PRIVATE_TOKEN = env_token if env_token else ''

    def __init__(self):
        self.url_class = None
        self.set_url_class()

    @abstractmethod
    def set_url_class(self):
        pass

    def do_collect(self, data_filter):
        requests.packages.urllib3.disable_warnings()
        page = 1
        data = []
        while True:
            url = self.url_class.collect_opened_page_url(
                str(page), data_filter.url_filter_str)
            print(url)
            resp = requests.get(url,
                                headers={'PRIVATE-TOKEN': self.PRIVATE_TOKEN},
                                verify=False)

            if resp.status_code in [401, 404, 403, 402]:
                raise ValueError(f'{resp.status_code} found')

            for _dict_data in resp.json():
                logging.error(_dict_data)
                data.append(self.parse_and_get_useful_data(_dict_data))

            if resp.headers.get('X-Next-Page', '') == '':
                break

            page += 1

        logging.info('#'*60)
        logging.info(f'{self.__class__.__name__[:-7]}处理的issue单：')
        logging.info(', '.join([str(issue.get('issue_id')) for issue in data]))
        logging.info('#'*60)

        return data

    def close_recorded_issue(self, data):
        for _data in data:
            issuse = _data.get('issue_id')
            url = self.url_class.close_issue_url(issuse)
            resp = requests.put(url,
                                headers={'PRIVATE-TOKEN': self.PRIVATE_TOKEN},
                                verify=False)
            url = self.url_class.add_label(issuse,
                                           'closed_by_xls_bot_and_recorded')
            resp = requests.put(url,
                                headers={'PRIVATE-TOKEN': self.PRIVATE_TOKEN},
                                verify=False)
            logging.info(f'close issue {issuse} success' )

    @abstractmethod
    def parse_and_get_useful_data(self, dict_data):
        pass

    def _get_customer_from_description(self, data: dict):
        des = data.get('description', '').replace('\n', '')
        who = ''
        contact = ''
        if des:
            try:
                rets = des.split(':')[2]
                contacts = des.split(':')[3]

                who = re.search(r'(.*)\*.*', rets)[1]
                contact = re.search(r'(.*)\*.*', contacts)[1]
                if not who:
                    who = re.search(r'(.*)\*(.*)', rets)[2]
            except Exception as e:
                logging.warning(
                    f'Failed to parse description, issue is {data.get("iid")}, '
                    f'with repo {self.__class__.__name__[:-7]},details: {e}')

        who, contact = who.strip(), contact.strip()

        if '邮件日期' in contact:
            contact = contact.split('邮件日期')[0]

        if not contact and who:
            contact = who
        elif contact and not who:
            who = contact

        return who, contact

    def _get_our_answer(self, url):
        requests.packages.urllib3.disable_warnings()
        resp = requests.get(url,
                            headers={'PRIVATE-TOKEN': self.PRIVATE_TOKEN},
                            verify=False)
        ret = '已给客户发送解决方案'
        fenxi, jianyi = ret, ret
        for dict_data in resp.json():
            body = dict_data.get('body', '').strip()
            if not re.match(r'#{1,5} *分析.*', body):
                continue

            rets = re.split(r'#{1,5} *建议', body)

            if len(rets) == 2:
                fenxi, jianyi = rets

            fenxi, jianyi = re.sub(r'(\n*|`*|#*)', '', fenxi), re.sub(
                r'(\n*|`*|#*)', '', jianyi)

            if len(fenxi) >= 200:
                fenxi = fenxi[:200]
            if len(jianyi) >= 200:
                jianyi = jianyi[-200:]

        return fenxi, jianyi


class Ha28Collect(GitDataCollect):
    DEFAULT_ACTOR = ['杨应发', '徐云风', '黄家倍']

    def set_url_class(self):
        self.url_class = Ha28ActionUrl()

    def parse_and_get_useful_data(self, data: dict):
        ret = {}
        ret['issue_id'] = data.get('iid')
        ret['title'] = data.get('title')
        ret['answer_at'] = data.get('created_at', '').split('T')[0]
        ret['our_people'] = random.choice(self.DEFAULT_ACTOR) if not data.get(
            'assignees', []) else data.get('assignees', [])[0].get('name')
        who, contact = self._get_customer_from_description(data)
        ret['who'] = who
        ret['email'] = contact
        fenxi, jianyi = self._get_our_answer(
            self.url_class.get_issue_answer(ret.get('issue_id')))
        ret['fenxi'] = fenxi
        ret['jianyi'] = jianyi
        return ret


# 用户数据收集
class UserWantCollect(GitDataCollect):
    DEFAULT_ACTOR = ['杨应发', '徐云风', '黄家倍']

    def set_url_class(self):
        pass

    def parse_and_get_useful_data(self, dict_data):
        pass
