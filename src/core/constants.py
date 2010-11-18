'''
Created on 18 nov. 2010

@author: dad
'''

class Constants(object):
    '''
    Specify inherent constants
    '''
    HOST_MANAGER = 'localhost'
    HOST_PORT = 50007

    def __init__(self):
        '''
        Constructor
        '''
        
    def getHostManager(self):
        return Constants.HOST_MANAGER
    
    def getHostPort(self):
        return Constants.HOST_PORT