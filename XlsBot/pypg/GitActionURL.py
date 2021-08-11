#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: GitAction.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


def url_plus(*args):
    ret = '/'.join(args)

    return ret


class GitActionUrl:
    BASE_API_URL = ''
    REPO_ID = ''

    def __init__(self):
        api_url = url_plus(self.BASE_API_URL, 'api/v4/projects')
        self.url = url_plus(api_url, self.REPO_ID)

    def open_issue_url(self, issue):
        return url_plus(self.url, f'issues/{issue}?state_event=reopen')

    def close_issue_url(self, issue):
        return url_plus(self.url, f'issues/{issue}?state_event=close')

    def add_label(self, issue: str, label):
        if isinstance(label, list):
            label = ','.join(label)

        return url_plus(self.url, f'issues/{issue}?add_labels={label}')

    def collect_opened_page_url(self, page, labels=None):
        if not labels:
            return url_plus(self.url,
                            f'issues?state=opened&per_page=50&page={page}'
                            )

        if isinstance(labels, list):
            labels = ','.join(labels)

        return url_plus(self.url,
                        f'issues?state=opened&labels='
                        f'{labels}&per_page=50&page={page}'
                        )

    def get_issue_answer(self, issue):
        return url_plus(self.url, f'issues/{issue}/notes')


class SkybilityHaUrl(GitActionUrl):
    BASE_API_URL = 'https://gitlab.skybilityha.com'


class Ha25ActionUrl(SkybilityHaUrl):
    REPO_ID = '44'


class SuseActionUrl(SkybilityHaUrl):
    REPO_ID = '43'


class Ha28ActionUrl(SkybilityHaUrl):
    REPO_ID = '45'


# 用户新增url生成
class UserWantActionUrl(SkybilityHaUrl):
    pass
