#-*- coding:utf-8 -*-

import threading
import time

import urllib2



class ThreadList(object):
    __tlist={}
    __index=-1
    def __init__(self,num,threadtype,feed):
        self.__max=num
        self.__type=threadtype
        self.__feed=feed
        for i in range(num):
            
            tmpthread=self.__type()

            self.add(tmpthread)
            one = feed.get_one()
            while one==None:
                one=feed.get_one()
            threadtype.feed(one)

        pass

    def get_list(self):
        return self.__tlist
        

    def add(self,thread):
        self.__index+=1
        thread.reg(self,self.__index)
        thread.start()
        self.__tlist.update({self.__index:thread})

        return self.__index


class UrlDirName(threading.Thread):
    __id=''
    __feed=''
    __tlist=''
    __try_max=10
    __try_time=0

    def __init__(self):
        threading.Thread.__init__(self)
        self.__stop=threading.Event()
        


    def run(self):
        while True:
            
            if self.is_stop:
                
                if self.__tlist!='':
                    self.__tlist.worker_dead(self)

                return

            while self.__feed=='':
                print "thread %d is waiting to be feed" % self.__id

            line =self.__feed
            self.__feed=''
            url,directory,name=line.split(',')
            
            self.__download(url)
            
            

        pass

    def reg(self,tlist,tid):
        self.__tlist=tlist
        self.__id=tid
    
    def feed(self,data)
        pass

    def stop(self)
        self.__stop.set()


    def is_stop(self):
        return self.__stop.is_set()


    def __download(self,url):
        if self.__try_time< self.__try_max:
            try:
                data=urllib2.urlopen(url).read()
                print "downloaded at % try" % self.__try_time
                return data
            except:
                return self.__download(url)
            
        return None
            
