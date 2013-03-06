#-*- coding:utf-8 -*-

import threading
import time

import urllib2



class ThreadList(object):
    __tlist={}
    def __init__(self,num,threadtype,feed):
        self.__num=num
        self.__type=threadtype
        self.__feed=feed

        pass

    def get_list(self):
        return self.__tlist
        
        pass

    def add(self):
        tmpthread=self.__type()
        pass


class UrlDirName(threading.Thread):
    __id=''

    def __init__(self):
        threading.Thread.__init__(self)
        self.__stop=threading.Event()
        


    def run(self):

        pass
