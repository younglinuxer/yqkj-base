#!/usr/bin/env python
# -- coding:utf8 --
import os
import commands
import json
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def shell(cmd='uname -a'):
    return (os.system(cmd))


def r_shell(cmd='ls'):
    return commands.getstatusoutput(cmd)