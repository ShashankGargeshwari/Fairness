# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 17:16:18 2017

This is the main class that sets up the game, simulates it, displays it graphically and updates it
@author: shashank
"""

# Import all the prerequisites here

import gambit as gm
import graphics  as gr
import numpy as np
from graphics import *
from numpy import ndarray
import world
from world import cell
from world import food
from world import player
import random
import pygame

# Class that manages the game setup and update
class gamemanager(object):
    
    # Contains parameters used in the generation and simulation of the world 
    cellToPlayerRatio = 0.1
    foodSpawnChance = 0.2
    
    # Holds a list of all entities that have to be displayed
    allEntities = '' 
     
    # Contains the generative logic to set up the world with food, players and other objects that might be needed to start the simulation
    def __init__(self , window, xSize, ySize , ppu):
        self.win = window        
        xSize = xSize / ppu
        ySize = ySize / ppu
        # Create the matrix for the grid of cells
        self.grid = np.arange(xSize*ySize , dtype=object).reshape(xSize,ySize)
        
        # Create the list for the players playing the game
        self.players = np.arange(0 , dtype = object).reshape(0)
        
        
        pn = 0
        fn = 0        
        # Iterate through the matrix of cells and insert food or player in them
        for i in range(xSize):
            for j in range(ySize):
                r = random.randrange(0,50)
                self.grid[i][j] = cell(i , j , ppu)
                if random.randrange(100) < self.foodSpawnChance*100:
                    self.grid[i][j].insert(food(i,j,ppu))
                    print("Food Inserted" , i , j , fn)
                    fn = fn+1
                else:
                    if random.randrange(100) < self.cellToPlayerRatio*100:
                        p = player(i,j,ppu,100,100,100,50)
                        self.players = np.append(self.players, [p])
                        print("Player Inserted at " , i , j , len(self.players))
                        self.grid[i][j].insert(p)
                        
        print("Initialization Done...")
        for p in self.players:
            v = np.arange(25  , dtype=object).reshape(5,5)
            t = ""
            for i in range(-2,3):
                for j in range(-2,3):
                    print("i , j" , i ,  j)
                    # Check whether the cell is within the bounds of the grid
                    if p.x + i > -1 and p.x + i < xSize and  p.y + j > -1 and p.y + j < ySize:
                        # If within bounds, ping cell, figure out which entity occipies it, put it in the vision matrix
                        e = self.grid[p.x+i][p.y+j].ping()
                        
                        if len(e) > 0:
                            if e[0] is player:
                                t = "p"
                            elif e[0] is food:
                                t = "f"
                        else:
                            t = "c"
                    else:
                        t = "n"
                    v[j+2][i+2] = t
                    
            p.simulateGame(v)
                
      
    # render the game to the graphical window 
    def display(self):
       for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i][j].display(self.win)
                
                
        
    
    class environment:
        pass
    
    def update(self):
        for p in self.players:
            
            pass
        
    

   
def main():
   print("Running Main function in gamemanager")   