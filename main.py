# -*- coding:utf-8 -*-


import time
import threads
from sys import argv
import os
import feeder

script,param=argv


thread_num=3

if os.path.exists(param) is False:
    raise SystemError("File not exist")

if os.path.exists('tmp') is False:
    os.makedirs('tmp')


feed=feeder.Feeder(param)
feed.start()


tlist=threads.ThreadList(thread_num,threads.UrlDirName,feed)



while True:
    time.sleep(5)
