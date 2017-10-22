# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:34:54 2017
A basic 2D entity in the world.
What are the important attributes of such an entity?

1) Location (Even though it may not be aware of it)
2) Representation (How the given entity must be displayed)
3) Pretty much it, right?
 
@author: shashank
"""

import graphics as gr

class entity(object):
    
    pixelsPerUnit = 1
    
    # Initialize each entity with x y co-ordinates and pixel density
    def __init__(self,x,y,p):
        self.x = x
        self.y = y
        self.setPPU(p)
    
    # Method to set Pixels per unit of all class instances that inherit from entity
    @classmethod
    def setPPU(cls,p):
        cls.pixelsPerUnit = p
    # Display the entity onto the Graphic Window passed to it
    def display(self , win):
        c = Circle(point(x,y) , 0)
        c.display(win)
        
    # Abstract method to update each entity after each framed  
    def update(self):
        pass
