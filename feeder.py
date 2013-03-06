# -*- coding:utf-8 -*-


import time
import threading


class Feeder(threading.Thread):
    

    __buff=[]
    buff_size=1000
    def __init__(self,filename):
        threading.Thread.__init__(self)

        self.__fp=open(filename,'r')


    def run(self):
        while True:
            while len(self.__buff) < self.buff_size:
                line=self.__fp.readline()
                if line!='':
                    self.__buff.append(line)

            time.sleep(5)

    def get_one(self):
        if self.__buff=[]:
            return None
        
        line=self.__buff.pop(0)
        return self.__handle(line)
    

    def __handle(self,line):
        if line[-1]== '\n':
            line=line[:-1]
        return line


        
