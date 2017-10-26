# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 18:37:20 2017
Contains classes related to the world the game is supposed to take place in
@author: shashank
"""
import numpy as np
import gambit as gm
from gambit import *
from gambit import nash
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
      
      
    # Method to insert an entity into the given cell
    def insert(self,s):
        self.entities.append(s)
        # print("Inserted Food into cell")
        return self
    
    def remove(self,a):
        if len(self.entities) != 0:
            print("Something is there")
        
    def display(self,win):
        super(cell,self).display(win)
        if len(self.entities) != 0:
           for e in self.entities:
              e.display(win)
    
    def ping(self):
        return self.entities
               
               
       
class player(entity):
    state = 0 #Maintains the current state of the player
    
    # Defines the various 2D movements that the player can perform
    optionMovement = {  0:(-1,-1) , 1:(0,-1) , 2:(1,-1) ,
                        3:(-1,0)  , 4:(0,0)  , 5:(1,-0) ,
                        6:(-1,1)  , 7:(0,1)  , 8:(1,1)   }
                        
    #constructor to set stats of the player
    def __init__(self, x, y, p, he, ha, en, ki):
        super(player,self).__init__(x,y,p)
        self.health = he
        self.happiness = ha
        self.energy = en
        self.kindness = ki
       
                     
        # Display the player in the world 
    def display(self,win):
        super(player,self).display(win)
           
            
    # Function to evaluate current state of the player, it's neighbours, then take a corresponding action based on these details
    def simulateGame(self,vision):
        # Vision is a 5x5 matrix of all the objects around the player
              
        # Add the player right at the start to give it the coveted position number 1      
        players = [vision[2][2].entities[0]]
        playerCount = [9]
        dimension = []
        
        # Count the number of players to set up the game
        for i in range(5):
            for j in range(5):
                if vision[i][j] != None and len(vision[i][j].entities) > 0 and isinstance( vision[i][j].entities[0] , player) and vision[i][j].entities[0] != self:
                    playerCount.append(9)
                    players.append(vision[i][j].entities[0])
                                        
                    
                
        # Start constructing the table
        g = gambit.new_table(playerCount)
        g.title = "Game for Player [" + str(self.x) + " , "+ str(self.y) + "] vs " + str(len(playerCount) - 1) + " Players."
        print("Simulating" + g.title)
        print("Co-ordinates of other entities will be displayed relative to self player from this point onwards.")        
        
        dimension = playerCount[:]
        playerCount = len(playerCount)
        
        # Set strategy labels and indices for all players                
        for p in players:
            i = players.index(p)
            
            # Set strategy indices and labels
            for c in range(9):
                g.players[i].strategies[c].label = "Move <" + str(self.optionMovement[c][0]) + "," + str(self.optionMovement[c][1]) + ">" 
                               
            if(i == 0):
                g.players[i].label = "Self player"
                # Since the self player is already added at the coveted 0 index, leave it out
                continue
            g.players[i].label = "Player at [" + str(p.x-self.x) +  "," + str(p.y-self.y) + "]"
            print("    " + g.players[i].label)
            
# Class that represents the food in the game world
class food(entity):
    
    def __init__(self,x,y,p):
        super(food,self).__init__(x,y,p)
        
    def display(self,win):
        super(food,self).display(win)
        
        
    
    
    