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
import random

# Class that holds the game and player states
class game:
       
    # Contains the generative logic to produce a grid of cells | logic can be changed later
    def __init__(self , window, xSize, ySize , pSize):
        self.win = window        
        self.grid = np.arange(xSize*ySize , dtype=object).reshape(xSize,ySize)
        self.players = np.arange(pSize).reshape(pSize)
        print(xSize,ySize)
        for i in range(xSize):
            for j in range(ySize):
                r = random.randrange(0,50)
                self.grid[i][j] = cell().insert(r)
                print(r)
        print("--------------------------------------")
                
      
    # render the game to the graphical window 
    def display(self):
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                c = Circle(Point( i * 10 , j * 10) , self.grid[i][j].entity)
                c.draw(self.win)
                print(self.grid[i][j].entity)
                        
    
    class environment:
        pass
    
    def update(self):
        for i in range(self.players.size):
          #  self.players[i].update()
            pass
        
    
class player:
    state = 0 #Maintains the current state of the player
    x = 0
    y = 0
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
   
def main():
    win = GraphWin("Game" , 300 , 200)
    g = game(win,3,2,10)
    g.display()
    win.getMouse()
    win.close()
            
if __name__ == '__main__':       
     main()       