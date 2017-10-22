# Fair World
## Summary
An experimental society where interactions between beings are determined by a game theoretic model of fairness. Can be inculded in the rhetoric of Artificial Life.

## Model
* ### Game Manager
  The game manager manages the entire setup and simulation of the game. It holds hooks to all the cells and entities and simulates them over time accordingly.
* ### World
  The world in which the simulation takes place is a grid of rectangular cells. Entities spawn, move around and interact at a     resolution defined by this grid of cells.

  *   #### Cells
      A cell is the basic unit of space in the simulation. Each cell is a given location on the map and can accomodate atmost 1       entity in it.

* ### Entities
  Entities are the bare minimum objects in the world, defined by a location and a visual representation. These entities can       later be moulded into more complex objects (example: food , creatures, barriers, etc)

  * #### Players
    A Player is an entity in the game that is trying to maximize gains under conflict in the world. This conflict may be           between other players, the environment, or itself(whatever that means). Importantly, each player will have 
    * Choices
    * Energy to execute these choices
    * Happiness to determine the effectiveness of a choice

   * #### Food
     Food provides players with energy, and a little happiness. 
