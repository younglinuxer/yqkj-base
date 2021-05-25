#!/usr/bin/env python
# -- coding:utf8 --
import os
import commands
import json


def shell(cmd='uname -a'):
    print(os.system(cmd))


def r_shell(cmd='ls'):
    return commands.getstatusoutput(cmd)