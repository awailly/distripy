'''
Created on 18 nov. 2010

@author: dad
'''

import socket
import pickle
from core.constants import Constants
from core.segment import Segment
from core.tools import *

class Manager(object):
    '''
    Create an instance of a distributed Manager
    '''

    def __init__(self, start, stop, segmentSize, hash):
        '''
        Constructor
        '''
        self.HOST = ''
        self.PORT = Constants.getHostPort(self)
        self.START = start
        self.STOP = stop
        self.SEGMENT_SIZE = segmentSize
        self.CURRENT = self.START
        self.HASH = hash
        self.resultTable = dict()
        
    def generateNextSegment(self):
        '''
        Normal condition
        '''
        segmentCurrent = ""
        
        if self.CURRENT < self.STOP:
            segmentCurrent = Segment(self.CURRENT, self.CURRENT + self.SEGMENT_SIZE, self.HASH)
            self.CURRENT = self.CURRENT + self.SEGMENT_SIZE
        else:
            '''
            Test if there's a missing segment
            '''
            for i in range(self.START, self.STOP, self.SEGMENT_SIZE):
                if not i in self.resultTable:
                    segmentCurrent(i, i + self.SEGMENT_SIZE, self.SEGMENT_SIZE, self.HASH)
            '''
            Send final segment
            '''
            if segmentCurrent == "": segmentCurrent = Segment(self.STOP, self.STOP, self.HASH)
            
        return segmentCurrent
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("[x] Binding")
        s.bind((self.HOST, self.PORT))
        print("[x] Listening")
        s.listen(1)
        
        finalResult = ""
        
        while True:
            if len([i for i in range(self.START, self.STOP, self.SEGMENT_SIZE) if not i in self.resultTable.keys()]) == 0:
                break
            print("[x] Accepting")
            conn, addr = s.accept()
            
            print("[x] Grabbing data")
            data = Tools.getDataFromSocket(conn)
            
            '''
            Protocol abstract
            '''
            if data == b"Hello, world":
                print("[x] Node " + str(addr) + " requesting new segment")
                data = pickle.dumps(self.generateNextSegment())
                if not data: break
                conn.send(data)
                conn.close()
            elif data == b"Result":
                print("[x] Node " + str(addr) + " sending result")
                dataResult = pickle.loads(Tools.getDataFromSocket(conn))
                self.resultTable[dataResult.START] = 1
                strResult = dataResult.RESULT
                print("[+] :: " + str(strResult))
                if strResult != "": finalResult += str(strResult) + "\n"
                conn.close()
                
        print("[+] Final results: " + finalResult)

if __name__ == "__main__":
    managerCurrent = Manager(0, 10000, 1000, 111)
    managerCurrent.run()