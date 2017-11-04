# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 18:37:20 2017
Contains classes related to the environment and the agents that inhabit the world
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
from copy import copy, deepcopy
import random


class world:
    entities = 0


class cell(entity):
    # Holds the sprite that has to be displayed
    sprite = 0

    # Holds an entity that is currently occupying the cell. If no entity, it holds the string nothing

    # Constructor to set state of a cell
    def __init__(self, x, y, p):
        # super( x , y , p)
        super(cell, self).__init__(x, y, p)
        self.entities = []
        # print("Count" , len(self.entities))

    # Method to insert an entity into the given cell
    def insert(self, s):
        self.entities.append(s)
        # print("Inserted Food into cell")
        s.x = self.x
        s.y = self.y
        if isinstance(s, scent) and any(isinstance(x, scent) for x in self.entities):
            for a in self.entities:
                if isinstance(a, scent) and a != s:
                    self.remove(a)
                    s.strength = s.strength + a.strength
        return self

    # Method to remove an entity that inhabits a cell
    def remove(self, a):
        if len(self.entities) != 0:
            print("Something is there")
            self.entities.remove(a)

    # Display the cell and all entities that it contains
    def display(self, win):
        super(cell, self).display(win)
        if len(self.entities) != 0:
            for e in self.entities:
                e.update()
                e.display(win)

    # return all entities that a cell
    def ping(self):
        return self.entities

    # return all entities of a particular type that a cell has
    def ping(self, cls):

        temp = []
        for e in self.entities:
            if isinstance(e, cls):
                temp.append(e)

        return temp


# Class that represents the players / agents in the world
class player(entity):
    state = 0  # Maintains the current state of the player

    #Define payoffs for different situations
    food_payoff = 10
    death_payoff = -99
    scent_payoff = -1

    # Defines the various 2D movements that the player can perform (Valid strategies in Game Theory terms)
    optionMovement = {0: (-1, -1), 1: (0, -1), 2: (1, -1),
                      3: (-1, 0), 4: (0, 0), 5: (1, 0),
                      6: (-1, 1), 7: (0, 1), 8: (1, 1)}

    # constructor to set stats of the player
    def __init__(self, x, y, p, he, ha, en, ki):
        super(player, self).__init__(x, y, p)
        self.health = he
        self.happiness = ha
        self.energy = en
        self.kindness = ki
        self.nextOption = None

    # Display the player in the world
    def display(self, win):
        super(player, self).display(win)

    # Eat something that is passed to the player
    def eat(self, f):
        self.health = self.health + 10
        if self.health > 100:
            self.health = 100

    # Move the player based on next option computed
    def move(self, grid, players):

        # Decrement energy because each move takes energy
        self.energy = self.energy - 10

        # Remove oneself from the current cell and leave a scent behind in the cell
        grid[self.x][self.y].remove(self)
        grid[self.x][self.y].insert(scent(0, 0, self.pixelsPerUnit, id(self)))
        print("Error point", self.x + self.nextOption[0], self.y + self.nextOption[1])

        # Insert onself into the new cell
        grid[self.x + self.nextOption[0]][self.y + self.nextOption[1]].insert(self)

        # Evalute the new cell
        otherPlayers = []
        foods = []

        # Poll all the players and food particels in the current cell
        for e in grid[self.x][self.y].entities:
            if isinstance(e, food):
                foods.append(e)
            elif isinstance(e, player):
                otherPlayers.append(e)

        # If there are other players, kill all players in the current cell
        if len(otherPlayers) > 1:
            for p in otherPlayers:
                grid[self.x][self.y].remove(p)
                #players = np.delete(players, p)
                players = players[players != p]

        # if there is food, consume it
        elif len(foods) > 0:
            for f in foods:
                self.eat(f)
                grid[self.x][self.y].remove(f)

    # Function to evaluate current state of the player, it's neighbours, then take a corresponding action based on
    # these details
    def simulate_game(self, vision):
        # Vision is a 5x5 matrix of all the objects around the player
        future_sight = deepcopy(vision)

        # Add the player right at the start to give it position number 0
        players = [vision[2][2].entities[0]]

        # Array to set up dimension (number of players) and shape (Number of choices each player can take)
        player_count = [9]
        dimension = [8]

        # Count the number of players to set up the game
        for i in range(5):
            for j in range(5):
                if vision[i][j] is not None and len(vision[i][j].entities) > 0 and isinstance(vision[i][j].entities[0], player) and vision[i][j].entities[0] != self:
                    player_count.append(9)
                    players.append(vision[i][j].entities[0])
                    dimension.append(8)

        # Start constructing the table
        g = gambit.new_table(player_count)
        g.title = "\n \nGame for Player [" + str(self.x) + " , " + str(self.y) + "] vs " + str(
            len(player_count) - 1) + " Players."
        print("Simulating" + g.title)
        print("Co-ordinates of other entities will be displayed relative to self player from this point onwards.")

        player_count = len(player_count)

        # Set strategy labels and indices for all players                
        for p in players:
            i = players.index(p)

            # Set strategy indices and labels
            for c in range(9):
                g.players[i].strategies[c].label = "Move [" + str(self.optionMovement[c][0]) + "," + str(
                    self.optionMovement[c][1]) + "]"

            # Condition to handle if the current player to be processed is the self
            if (i == 0):
                g.players[i].label = "Self player"
                # Since the self player is already added at the coveted 0 index, leave it out
                continue
            g.players[i].label = "Player at [" + str(p.x - self.x) + "," + str(p.y - self.y) + "]"
            print("    " + g.players[i].label)

        # Now this is the tough part. Construct the payoffs
        # g[0,0][0] = 8
        #   ^    ^   
        #   |    which player's payoff it is
        #   |
        #   same dimensions as number of players
        g[dimension][0] = 2

        # The list generates all possible combinations of choices | all_player_choices contains ONE combination of the choices of all players | this_players_choice is the choice of each player
        for all_player_choices in list(it.product(*[range(9)] * player_count)):
            future_sight = deepcopy(vision)
            future_sight_players = [future_sight[2][2].ping(player)[0]]

            # Assign future_sight players
            # future_sight_players.append(future_sight[2][2].entities[0])
            for i in range(5):
                for j in range(5):
                    if i == 2 and j == 2:
                        continue
                    c = future_sight[i][j]

                    if c is not None and len(c.entities) > 0:
                        if isinstance(c.entities[0], player):
                            future_sight_players.append(c.entities[0])

            # Iterate through individual choices of each player and update their position assuming that choice is made
            for i, this_players_choice in enumerate(all_player_choices):
                current_player = future_sight_players[i]

                # remove player from current list
                future_sight[current_player.x - self.x + 2][current_player.y - self.y + 2].entities.remove(current_player)

                # Calculate new x,y for player based on the choice it made in the current combination
                newX = current_player.x - self.x + self.optionMovement[this_players_choice][0] + 2
                newY = current_player.y - self.y + self.optionMovement[this_players_choice][1] + 2

                # If new location is still within the future vision, add it to the cell at the new location 
                if newX > -1 and newX < 5 and newY > -1 and newY < 5:
                    if future_sight[newX][newY] is not None:
                        future_sight[newX][newY].insert(current_player)
                    else:
                        current_player.payoff = -999
                else:
                    current_player.payoff = -20

            # All movement made, evaluate the payoffs for each player and store it
            for i in range(5):
                for j in range(5):
                    if future_sight[i][j] is None:
                        continue
                    if len(future_sight[i][j].entities) > 0:
                        foodInCell = []
                        playersInCell = []
                        for e in future_sight[i][j].entities:
                            if isinstance(e, player):
                                playersInCell.append(e)
                            elif isinstance(e, food):
                                foodInCell.append(e)

                            if len(playersInCell) > 1:
                                for pic in playersInCell:
                                    pic.payoff = -99
                            elif len(playersInCell) == 1:
                                playersInCell[0].payoff = 0
                                if len(foodInCell) > 0:
                                    playersInCell[0].payoff = 10
                                if len(future_sight[i][j].ping(scent)) > 0:
                                    for s in future_sight[i][j].ping(scent):
                                        playersInCell[0].payoff = playersInCell[0].payoff - s.strength / 100

                                temp = 0
                                for w in range(-1, 2):
                                    for h in range(-1, 2):
                                        if i + w > -1 and i + w < 5 and j + h > -1 and j + h < 5:
                                            if future_sight[i + w][j + h] is not None:
                                                if len(future_sight[i + w][j + h].entities) > 0:
                                                    for e in future_sight[i + w][j + h].entities:
                                                        if isinstance(e, food):
                                                            temp = temp + 1
                                playersInCell[0].payoff = playersInCell[0].payoff + temp
                                # Now this is the tough part. Construct the payoffs :\
            # g[0,0][0] = 8
            #   ^    ^   
            #   |    which player's payoff it is
            #   |
            #   same dimensions as number of players                                                                            
            for p in future_sight_players:
                print(p.payoff)
                g[all_player_choices][future_sight_players.index(p)] = p.payoff

                # Game Table is (Hopefully) filled with all the necessary values

        # Time to actually solve the game
        p = g.mixed_profile()

        # Getting to the actual solving part of gambit
        print("Soving the game for ", len(g.players), " Players")
        solver = gambit.nash.ExternalLogitSolver()
        solution = solver.solve(g)
        print("\n----------------------Game Solved")
        options = solution[0].__getitem__(g.players[0])
        agg = 0
        rand = random.random()
        self.nextOption = None
        print(options)
        i = -1
        op = []
        for o in options:
            i = i + 1
            agg = agg + o
            if agg > rand:
                self.nextOption = self.optionMovement[i]
                break
                # print(solver.solve(g))


# Class that represents the food in the game world
class food(entity):
    def __init__(self, x, y, p):
        super(food, self).__init__(x, y, p)

    def display(self, win):
        super(food, self).display(win)


# Class that represents scent left by a player        
class scent(entity):
    def __init__(self, x, y, p, pid):
        super(scent, self).__init__(x, y, p)
        self.playerID = pid
        self.strength = 100

    # def display(self, win):
    #    super(scent, self).display(win)

    def update(self):
        if self.strength > 0:
            self.strength = self.strength - 1
