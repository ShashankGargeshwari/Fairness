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
import random
import pygame

# Class that holds the game and player states
class gamemanager(object):
       
    # Contains the generative logic to produce a grid of cells | logic can be changed later
    def __init__(self , window, xSize, ySize , pSize):
        self.win = window        
        self.grid = np.arange(xSize*ySize , dtype=object).reshape(xSize,ySize)
        print(xSize,ySize)
        for i in range(xSize):
            for j in range(ySize):
                r = random.randrange(0,50)
                self.grid[i][j] = cell(i , j , pSize)
                if random.randrange(20) < 5:
                    self.grid[i][j].insert(food(i,j,pSize))
        print("Initialization Done...")
                
      
    # render the game to the graphical window 
    def display(self):
       for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i][j].display(self.win)
                
                
        
    
    class environment:
        pass
    
    def update(self):
        for i in range(self.players.size):
          #  self.players[i].update()
            pass
        
    

   
def main():
   print("Running Main function in gamemanager")   