# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 18:37:20 2017
Contains classes related to the world the game is supposed to take place in
@author: shashank
"""
import numpy as np
from entity import entity
import graphics as gr
from graphics import *

class world:
    entities = 0

class cell(entity):

    #Holds the sprite that has to be displayed
    sprite = 0    
    
    # Holds an entity that is currently occupying the cell. If no entity, it holds the string nothing
    
    # Constructor to set state of a cell
    def __init__(self , x , y  ,p):
       # super( x , y , p)  
        super(cell ,self).__init__(x,y,p)
        self.entities = []
        # print("Count" , len(self.entities))
      
    @classmethod
    def setSprite(cls,img):
        cls.sprite = img
    
    # Method to insert an entity into the given cell
    def insert(self,s):
        self.entities.append(s)
        # print("Inserted Food into cell")
        return self
    
    def remove(self,a):
        if len(self.entities) != 0:
            print("Something is there")
        
    def display(self,win):
        #win.blit(self.sprite , (self.x , self.y))   
        super(cell,self).display(win)
        if len(self.entities) != 0:
           for e in self.entities:
               e.display(win)
       
class player(entity):
    state = 0 #Maintains the current state of the player
   
   #class that mentions player stats and such. These might later be summarized into the "state" of the player
    class stats:
        health = 100
        happiness = 100
        energy = 100
        kindness = 100
        
        #constructor to set stats of the player
        def __init__(this, he, ha, en, ki):
            health = he
            happiness = ha
            energy = en
            kindness = ki
            
        
            
    # Function to evaluate current state of the player, it's neighbours, then take a corresponding action based on these details
    def nextAction():
       pass

class food(entity):
    
    def __init__(self,x,y,p):
        super(food,self).__init__(x,y,p)
        
    def display(self,win):
        super(food,self).display(win)
        
    
    
    