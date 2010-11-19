'''
Created on 18 nov. 2010

@author: dad
'''

class Status:
    TODO = 0
    FINISHED = 1
    
class Segment(object):
    '''
    Specify the segment of calculus for a specific computer
    '''


    def __init__(self, start, stop, hash):
        '''
        Constructor
        '''
        self.START = start
        self.STOP = stop
        self.HASH = hash
        self.STATUS = Status.TODO
        self.RESULT = ""
        
    def string(self):
        return "[" + str(self.START) + ", " + str(self.STOP) + "]"
    
        