#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: Log.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import logging
import os
import pathlib
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler


class SelfHandler(RotatingFileHandler):
    pass


class BindLog(ABC):
    def __init__(self, logger, loglevel):
        self.logger = logger
        self.loglevel = loglevel
        self.formatter = None
        self.handler = None

    @abstractmethod
    def _formatter(self):
        pass

    @abstractmethod
    def _handler(self):
        pass

    def bind(self):
        self._formatter()
        self._handler()

        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(self.loglevel)
        self.logger.addHandler(self.handler)


class BindStreamLog(BindLog):
    def _formatter(self):
        self.formatter = logging.Formatter(
            '%(asctime)s <%(levelname)s> %(message)s')

    def _handler(self):
        self.handler = logging.StreamHandler()


class BindFileLog(BindLog):
    def _formatter(self):
        self.formatter = logging.Formatter(
            '%(asctime)s [%(name)s]: <%(levelname)s> %(message)s '
            '[%(filename)s:%(lineno)d:%(funcName)s]')

    def _handler(self):
        file_name = pathlib.Path(__file__).parent.parent.absolute().as_posix() + '/log'
        os.makedirs(file_name, int('0755', 8), exist_ok=True)
        self.handler = SelfHandler(f'{file_name}/issue.log',
                                   maxBytes=10 * 1024 * 1024)


class XlsLog:
    def init_log(self, logtype='stdout', loglevel=logging.INFO):
        logger = logging.getLogger()

        if logger.hasHandlers():
            return

        if not logtype:
            return

        if isinstance(logtype, str):
            logtype = [logtype]

        logger.setLevel(logging.DEBUG)
        for t in logtype:
            if t == 'stdout':
                BindStreamLog(logger, loglevel).bind()
            else:
                BindFileLog(logger, loglevel).bind()
                logger.name = t
