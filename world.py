# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 18:37:20 2017
Contains classes related to the world the game is supposed to take place in
@author: shashank
"""
import numpy as np

class cell:
    # Holds an entity that is currently occupying the cell. If no entity, it holds the string nothing
    entity = 0
    # Constructor to set state of a cell
    def __init__(self):
        self.entity = 0
    
    @classmethod    
    def insert(self,s):
        self.entity = s
        return self
        
    
    
    
    