#import all pre-requisites

from gambit import *
from gambit import nash
from graphics import *

#Create new, trivial strategic form game with [n,n] strategies
g = gambit.new_table([2,2])

#Label game, players and strategies

g.title = "A fight for survival"
g.players[0].label = "Refugee"
g.players[1].label = "Army Officer"

g.players[0].strategies[0].label = "Kill"
g.players[0].strategies[0].label = "Leave"

g.players[1].strategies[1].label = "Kill"
g.players[1].strategies[1].label = "Leave"

#Assign strategies in the form g[strategy o p1 , strategy of p2][payoff for player #]
g[0,0][0] = 8
g[0,0][1] = 4
g[0,1][0] = 2
g[0,1][1] = 10
g[1,0][0] = 3
g[1,0][1] = 2
g[1,1][0] = 2
g[1,1][1] = 5


#Contingencies are the combinations of all strategies by players
for profile in g.contingencies:
    print profile, g[profile][0] , g[profile][1]

#Playing around with mixed strategies
p = g.mixed_profile()

#Initially spreads out probabilities evenly across all actions
print(list(p))

#Get expected payoff using MixedProfile.payoff(player)
print("Probability mixed strategy payoff of Player 1" )
print(p.payoff(g.players[0]))
print("Probability mixed strategy payoff of Player 2" )
print(p.payoff(g.players[1]))


#Get stand alone payoff value (whatever that means)
print(p.strategy_value(g.players[0].strategies[1]))

#Getting to the actual solving part of gambit
solver = gambit.nash.ExternalEnumMixedSolver()
print(solver.solve(g))

