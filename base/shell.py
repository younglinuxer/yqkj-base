#!/usr/bin/env python
# -- coding:utf8 --
import os
import commands


def shell(cmd='uname -a'):
    print(os.system(cmd))
