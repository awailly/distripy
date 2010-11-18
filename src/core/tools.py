'''
Created on 18 nov. 2010

@author: dad
'''

import socket

class Tools(object):
    '''
    Differents tools
    '''
        
    def getDataFromSocket(sck):
        while 1:
            line = ""
            line = sck.recv(1024)
            
            if len(line) < 1024:
                return line
