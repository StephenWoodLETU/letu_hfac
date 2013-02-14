# Abstract class for controlling the variable load

import abc

class LoadControl(object):
        __metaclass__ = abc.ABCMeta
        
        @abc.abstractmethod
        def setRLC(self, r, l, c):
            """Set the RLC of the variable load"""
            return
        
        @abc.abstractmethod
        def reset(self):
            """Set the load to zero impedence"""
            return

