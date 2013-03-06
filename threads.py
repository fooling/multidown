#-*- coding:utf-8 -*-

import threading
import time
import os

import urllib2



class ThreadList(object):
    __tlist={}
    __index=-1
    __fail_data=[]
    def __init__(self,num,threadtype,feed):
        self.__max=num
        self.__type=threadtype
        self.__feed=feed
        for i in range(num):
            
            tmpthread=self.__type()
            self._add(tmpthread)

        pass
    def _get_feed(self):
        one=self.__feed.get_one()
        while one==None:
            one=self.__feed.get_one()
        return one
            


    def _get_list(self):
        return self.__tlist
        

    def _add(self,thread):
        self.__index+=1
        thread._reg(self,self.__index)
        thread.start()
        self.__tlist.update({self.__index:thread})
        one =self._get_feed()
        thread._feed(one)

        return self.__index


    def _del(self,thread):
        thread.stop()
        tid=thread._get_id()
        del self.__tlist[tid]

    def _worker_dead(self,worker):
        self._del(worker)
        if len(self.__tlist)<self.__max:
            self._add(self.__type())
            
    def _worker_fail(self,worker,data):
        self._worker_dead(worker)
        self.__fail_data.append(data)
        print "fail list : ",self.__fail_data
            
    def _job_finished(self,worker):
        one=self._get_feed()
        worker._feed(one)
        


class UrlDirName(threading.Thread):
    __id=''
    __feed=''
    __tlist=''
    __try_max=10
    __try_time=0

    def __init__(self):
        threading.Thread.__init__(self)
        self.__stop=threading.Event()

        self.daemon=True
        


    def run(self):
        while True:
            
            if self.is_stop(): 
                print "thread %d is stoped",self.__id
                if self.__tlist!='':
                    self.__tlist._worker_dead(self)

                return

            while self.__feed=='':
                print "thread %d is waiting to be feed..." % self.__id
                time.sleep(2)


            line =self.__feed
            self.__feed=''
            url,directory,name=line.split(',')

            directory='tmp/'+directory
            path=directory+'/'+name+url.split('/')[-1]
            
            if os.path.exists(path):
                print "duplicate file",path
                self.__tlist._worker_fail(self,url)
                return

            print "starting to download ",url
            
            tmpfile=self.__download(url)
            if tmpfile==None:
                self.__tlist._worker_fail(self,url)
                return
            
            print url,"downloaded"

            if os.path.exists(directory) is False:
                os.makedirs(directory)

            
            try: 
                tmpfp=open(path,'wb')
                tmpfp.write(tmpfile)
                tmpfp.close()
            except:
                self.__tlist._worker_fail(self,url)
            
            self.__tlist._job_finished(self)
            
            

    def _get_id(self):
        return self.__id

    def _feed(self,data):
        self.__feed=data

    def _reg(self,tlist,tid):
        self.__tlist=tlist
        self.__id=tid
    

    def stop(self):
        self.__stop.set()


    def is_stop(self):
        return self.__stop.is_set()


    def __download(self,url):

        for i in range(self.__try_max):
            try:
                return urllib2.urlopen(url).read()
            except:
                pass
        return None
