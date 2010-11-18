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

    def __init__(self, start, stop, segmentSize):
        '''
        Constructor
        '''
        self.HOST = ''
        self.PORT = Constants.getHostPort(self)
        self.START = start
        self.STOP = stop
        self.SEGMENT_SIZE = segmentSize
        self.CURRENT = self.START
        
    def generateNextSegment(self):
        if self.CURRENT < self.STOP:
            segmentCurrent = Segment(self.CURRENT, self.CURRENT + self.SEGMENT_SIZE)
            self.CURRENT = self.CURRENT + self.SEGMENT_SIZE
        else:
            segmentCurrent = Segment(self.STOP, self.STOP)
        return segmentCurrent
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print("[x] Binding")
        s.bind((self.HOST, self.PORT))
        print("[x] Listening")
        s.listen(1)
        while True:
            print("[x] Accepting")
            conn, addr = s.accept()
            
            print("[x] Grabbing data")
            data = Tools.getDataFromSocket(conn)
            
            '''
            Protocol abstract
            '''
            if data == b"Hello, world":
                print("[x] Node " + str(addr) + " requesting new segment")
                        
                # print("[x] Connected by", addr)
                data = pickle.dumps(self.generateNextSegment())
                if not data: break
                conn.send(data)
                conn.close()
            elif data == b"Result":
                print("[x] Node " + str(addr) + " sending result")
                dataResult = Tools.getDataFromSocket(conn)
                print("[+] :: " + str(dataResult))
                conn.close()

if __name__ == "__main__":
    managerCurrent = Manager(0, 10000, 1000)
    managerCurrent.run()