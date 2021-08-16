#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: Action.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import logging
import sys
import pathlib
import os
from argparse import ArgumentParser

import argcomplete as argcomplete

os.environ["COMP_WORDBREAKS"] = " \t\"'@><=;|&("


def set_sys_path():
    cwd = pathlib.Path(__file__).parent.parent.absolute().as_posix()
    sys.path.insert(0, cwd + '/pypg')


set_sys_path()

import Log
from ExcelActor import ExcelActor

xlog = Log.XlsLog()
xlog.init_log(logtype=['stdout', os.getenv('I_WANT_EXCEL', 'sky_gitlab_robot')])

from DataCollect import Ha28Collect
from DataFilter import DataFilter
from DataTransefer import DataTransfer


def main(args):
    # 用户新增数据收集的自定义
    v_to_v = {'ha2.8': Ha28Collect()}

    family = args.repo.lower()
    labels = args.labels
    file_name = args.file

    try:
        with DataTransfer(host=os.getenv('HOSTS'),
                          username='root', passwd='fake123') as dt:
            dt.download_file(file_name, file_name)
            filter = DataFilter(labels)
            data = v_to_v.get(family).do_collect(filter)

            ex = ExcelActor(file_name, data=data, family=family)
            ex.do()
            dt.upload_file(file_name, file_name)
    except Exception as e:
        logging.error(f'{e}')
        return 1

    else:
        v_to_v.get(family).close_recorded_issue(data)

    return 0


def init():
    parser = ArgumentParser()
    parser.add_argument('--repo', required=True, action='store',
                        help="The class of xls you want",
                        choices=['ha2.8', 'ha2.5', 'suse'])
    parser.add_argument('--labels', required=False, action='store',
                        help="customer record to write")
    parser.add_argument('--file', required=True, help="load the current config",
                        ).completer = argcomplete.FilesCompleter()
    parser.set_defaults(func=main)
    return parser


if __name__ == '__main__':
    parser = init()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    ret = args.func(args)
    sys.exit(ret)
