# -*- coding:utf-8 -*-



import threads
from sys import argv
import os

script,param=argv



if  os.path.exists(argv) is False:
    raise SystemError("File not exist")


