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
import itertools as it
from copy import copy,deepcopy

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
                        3:(-1,0)  , 4:(0,0)  , 5:(1,0) ,
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
    
    # Prepare the game table for the players
    def prepareGameTable(self,vision,g):
        print("\n\n ---Trying to prepare game table for player at" , self.x, self.y)
        print("Number of players in the game is" , len(g.players))
    
    
    # Function to evaluate current state of the player, it's neighbours, then take a corresponding action based on these details
    def simulateGame(self,vision):
        # Vision is a 5x5 matrix of all the objects around the player
        futureSight = deepcopy(vision)      
        
        # Add the player right at the start to give it the coveted position number 1      
        players = [vision[2][2].entities[0]]
        playerCount = [9]
        dimension = [8]
        
        # Count the number of players to set up the game
        for i in range(5):
            for j in range(5):
                if vision[i][j] != None and len(vision[i][j].entities) > 0 and isinstance( vision[i][j].entities[0] , player) and vision[i][j].entities[0] != self:
                    playerCount.append(9)
                    players.append(vision[i][j].entities[0])
                    dimension.append(8)                    
                    
                
        # Start constructing the table
        g = gambit.new_table(playerCount)
        g.title = "\n \nGame for Player [" + str(self.x) + " , "+ str(self.y) + "] vs " + str(len(playerCount) - 1) + " Players."
        print("Simulating" + g.title)
        print("Co-ordinates of other entities will be displayed relative to self player from this point onwards.")        
        
        playerCount = len(playerCount)
        
        # Set strategy labels and indices for all players                
        for p in players:
            i = players.index(p)
            
            # Set strategy indices and labels
            for c in range(9):
                g.players[i].strategies[c].label = "Move [" + str(self.optionMovement[c][0]) + "," + str(self.optionMovement[c][1]) + "]" 
                               
            if(i == 0):
                g.players[i].label = "Self player"
                # Since the self player is already added at the coveted 0 index, leave it out
                continue
            g.players[i].label = "Player at [" + str(p.x-self.x) +  "," + str(p.y-self.y) + "]"
            print("    " + g.players[i].label)
        
        # Now this is the tough part. Construct the payoffs :\
        # g[0,0][0] = 8
        #   ^    ^   
        #   |    which player's payoff it is
        #   |
        #   same dimensions as number of players
        g[dimension][0] = 2
                       
        # The list generates all possible combinations of choices | k contains ONE combination of the choices of all players | l is one choice of each player
        for k in list(it.product(*[range(9)]*playerCount)):
            futureSight = deepcopy( vision )
            futureSightPlayers = [None]
            print("Current movement choice is",k)
            
            #Assign futureSight players
            futureSightPlayers[0] = futureSight[2][2].entities[0]
            for i in range(5):
                    for j in range(5):
                        if i == 2 and j == 2:
                            continue
                        c = futureSight[i][j]
                        
                        if c is not None and len(c.entities) > 0:
                            if isinstance( c.entities[0] , player):
                                futureSightPlayers.append( c.entities[0] )
                                
            #print("Options being chosen by players",k)
            # Iterate through individual choices of each player and update their position assuming that choice is made
            
            for i,l in enumerate(k):
                currentPlayer = futureSightPlayers[i]
                #print("l Value" , l , "i value" , i )
                #print("\nCurrently running game for Opponent" , currentPlayer.x , currentPlayer.y , "and Self" , self.x , self.y )
                    
                                
                futureSight[currentPlayer.x - self.x+2][currentPlayer.y - self.y+2].entities.remove(currentPlayer)
                
                # Calculate new x,y for player based on the choice it made in the current combination
                newX = currentPlayer.x - self.x + self.optionMovement[l][0] + 2
                newY = currentPlayer.y - self.y + self.optionMovement[l][1] + 2
                                
                # If new location is still within the future vision, add it to the cell at the new location 
                if newX > -1 and newX < 5 and newY > -1 and newY < 5 and futureSight[newX][newY] is not None:
                    futureSight[newX][newY].insert(currentPlayer)
                else:
                    currentPlayer.payoff = 0
                                
            # All movement made, evaluate the payoffs for each player and store it
            
            for i in range(5):
                for j in range(5):
                    if futureSight[i][j] is None:
                        continue
                    if len(futureSight[i][j].entities) > 0:
                        foodInCell = []
                        playersInCell = []
                        for e in futureSight[i][j].entities:
                            if isinstance(e,player):
                                playersInCell.append(e)
                            elif isinstance(e,food):
                                foodInCell.append(e)
                        
                            if len(playersInCell) > 1 :
                                for pic in playersInCell:
                                    pic.payoff = -9999
                                    print(futureSightPlayers.index(pic) , "Found Player, so payoff is -9999")
                            elif len(playersInCell) == 1:
                                if len(foodInCell) > 0:
                                    playersInCell[0].payoff = 20
                                    print(futureSightPlayers.index(playersInCell[0]),"Found food so payoff is 20")
                                else:
                                    playersInCell[0].payoff = -10
                                    print(futureSightPlayers.index(playersInCell[0]),"Found nothing, so payoff is -10")    
            # Now this is the tough part. Construct the payoffs :\
            # g[0,0][0] = 8
            #   ^    ^   
            #   |    which player's payoff it is
            #   |
            #   same dimensions as number of players                                                                            
            for p in futureSightPlayers:
                g[k][ futureSightPlayers.index(p)] = p.payoff                    
            
            # Game Table is (Hopefully) filled with all the necessary values     
        
        #  Time to actually solve the game
        p = g.mixed_profile()

        #Initially spreads out probabilities evenly across all actions
        #print(list(p))
        
        #Get expected payoff using MixedProfile.payoff(player)
        print("\n\nProbability mixed strategy payoff of Player Self at",self.x , self.y )
        print(p.payoff(g.players[0]))
                
        #Get stand alone payoff value (whatever that means)
        print("\nStandanlone payoff values")
        for i in range(9):
            print(p.strategy_value(g.players[0].strategies[1]))
        
        #Getting to the actual solving part of gambit
        solver = gambit.nash.ExternalEnumMixedSolver()
        print(solver.solve(g))
        #print(solver.solve(g))
            
# Class that represents the food in the game world
class food(entity):
    
    def __init__(self,x,y,p):
        super(food,self).__init__(x,y,p)
        
    def display(self,win):
        super(food,self).display(win)
        
        
    
    
    