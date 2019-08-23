#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2019 Tuhinshubhra

## OutSystems version detection
## Rev 1

import cmseekdb.basic as cmseek
import re


def start(id, source):
    version = '0'
    cmseek.statement('Detecting OutSystems Version')
    rr = re.findall(r'<script src=\"_osjs\.js\?(.*?)\"', source)
    if rr != []:
    	version = rr[0].replace("_",".")
    	cmseek.success(cmseek.bold + cmseek.fgreen + "Version Detected, OutSystems Version %s" % version + cmseek.cln)
    else:
    	cmseek.error("Couldn't Detect Version")
    return version