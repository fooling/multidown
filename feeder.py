# -*- coding:utf-8 -*-


import time
import threading


class Feeder(threading.Thread):
    

    __buff=[]
    buff_size=1000
    def __init__(self,filename):
        threading.Thread.__init__(self)
        self.__condition=threading.Condition()
        self.__buff_lock=threading.Lock()

        self.__fp=open(filename,'r')

        self.daemon=True


    def run(self):
        while True:
            #producer acquire condition
            self.__condition.acquire()
            print "feeder acquire condition"


            while len(self.__buff) < self.buff_size:
                line=self.__fp.readline()
                if line!='':
                    #acquire buff
                    self.__buff_lock.acquire()
                    #print "feeder acquire buff lock"
                    self.__buff.append(line)
                    #release buff
                    self.__buff_lock.release()
                    print "feed got",line
                    #notify condition
                    self.__condition.notify() 
                    #print "feeder notify condition"
                    continue
                #if nothing , go to sleep
                break

            #release
            self.__condition.release()
            print "feeder release condition"

            time.sleep(5)

    def get_one(self):
        self.__buff_lock.acquire()
        if self.__buff==[]:
            return None
        
        line=self.__buff.pop(0)
        self.__buff_lock.release()
        return self.__handle(line)

    def get_condition(self):
        return self.__condition
    

    def __handle(self,line):
        if line[-1]== '\n':
            line=line[:-1]
        return line


        
