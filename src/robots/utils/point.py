'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import math
class Point:

    def __init__(self, x, y, z=None):
        '''
        COnstructor
        :param x: coordinate in x axis
        :param y: coordinate in y axis
        :param z: coordinate in z axis
        '''
        self.x = round(x,2)
        self.y = round(y,2)
        if z is not None:
            z = round(z,2)
        self.z = z
        self.dims = [self.x, self.y, self.z]

    def __eq__(self, p):
        '''
        Equals method
        :param p:point
        :return: True if object passed as parameter is equals that these object
        '''
        if self.x == p.y and self.y == p.y:
            if self.z != None and self.z != self.z:
                return False
            return True
        return False

    def __hash__(self):
        return hash(str(self))