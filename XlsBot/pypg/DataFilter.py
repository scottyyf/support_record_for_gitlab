#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: DataFilter.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""


class DataFilter:
    def __init__(self, arg_in_str):
        self.other_label = arg_in_str

    @property
    def url_filter_str(self):
        if isinstance(self.other_label, str):
            return self.other_label
        elif isinstance(self.other_label, list):
            return ','.join(self.other_label)

        return 'Done'  # default
