#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: DataTransefer.py.py
Author: Scott Yang(Scott)
Email: yangyingfa@skybility.com
Copyright: Copyright (c) 2021, Skybility Software Co.,Ltd. All rights reserved.
Description:
"""
import os
import paramiko


class DataTransfer:
    def __init__(self, host, port=22, dkey="", username="", passwd="",
                 work_dir="/home"):
        self.host = host
        self.port = port
        self.dkey = dkey
        self.username = username
        self.passwd = passwd
        self.sftp = None
        self.transport = None
        self.work_dir = work_dir

        # paramiko.util.log_to_file('../log/paramiko_sftp.log')

    def prefix_login(self):
        self.transport = paramiko.Transport((self.host, self.port))
        if self.dkey:
            self.transport.connect(username=self.username, pkey=self.dkey)
        else:
            self.transport.connect(username=self.username, password=self.passwd)

        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.chdir(self.work_dir)

    def upload_file(self, local_file, remote_file):
        if not os.path.exists(local_file):
            return False

        self.sftp.put(local_file, remote_file)
        return True

    def download_file(self, remote_file, local_file):
        if remote_file not in self.sftp.listdir():
            return False

        self.sftp.get(remote_file, local_file)

    def __enter__(self):
        self.prefix_login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sftp:
            self.sftp.close()

        if self.transport:
            self.transport.close()
