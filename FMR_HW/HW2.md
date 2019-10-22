# Homework Problem 2

**Formal Methods in Robotics (Fall 2019)**



In this problem, we will implement the product of a Transition System (TS) and an Automaton (NFA). See Definition 4.16 from Principles of Model Checking by Baier and Katoen. 

To complete this HW, implement `product_tsys_aut()` function in `prod_ts_aut.py`. 



## Background

**Game Class:** Recall that the product operation of TS and NFA defines a game on graph. A game is represented by `class Game` in IGLSynth. The class definition is given in the `prod_ts_aut.py` for reference. Note that `Game` is a sub-class of `Graph` and, therefore, inherits all its methods and properties. It defines a `Game.Vertex` and `Game.Edge` classes to represent a vertex and edge of game, which must be used when adding vertices and edges to game in  `product_tsys_aut()` function. 

*Hint:* Do not forget to identify and mark the final vertices as final! See `final` property of `Automaton` class. 





