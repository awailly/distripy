'''
Created on 18 nov. 2010

@author: dad
'''

import socket
import pickle
from core.constants import Constants
from core.segment import Segment
from core.tools import Tools

class Client(object):
    '''
    Create an instance of a distributed client
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.HOST = Constants.getHostManager(self)
        self.PORT = Constants.getHostPort(self)
        
    def calcul(self, segment):
        '''
        Distributed program
        '''
        result = ""
        
        for i in range(segment.START, segment.STOP):
            if i == 5555:
                result += "Found hash with i = " + str(i)
        return result
        
    def run(self):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.HOST, self.PORT))
            print("[x] Sending")
            s.send(b"Hello, world")
            print("[x] Grabbing datas")
            data = Tools.getDataFromSocket(s)
            print("[x] Pickling")
            segmentToCompute = pickle.loads(data)
            print("[x] Closing connection")
            s.close()
            print("[x] Received segment", segmentToCompute.string())
            
            if segmentToCompute.START != segmentToCompute.STOP:
                print("[x] Calculating:")
                calculResult = self.calcul(segmentToCompute)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.HOST, self.PORT))
                print("[x] Sending result and closing connection")
                s.send(b"Result")
                s.send(bytearray(calculResult, encoding='ascii'))
                s.close()
                print("[x] Ended")
            else:
                print ("[x] End of segmentation reached, STOP")
                break

if __name__ == "__main__":
    clientCurrent = Client()
    clientCurrent.run()