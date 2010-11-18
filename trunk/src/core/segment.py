'''
Created on 18 nov. 2010

@author: dad
'''

class Segment(object):
    '''
    Specify the segment of calculus for a specific computer
    '''


    def __init__(self, start, stop):
        '''
        Constructor
        '''
        self.START = start
        self.STOP = stop
        
    def string(self):
        return "[" + str(self.START) + ", " + str(self.STOP) + "]"
    
        