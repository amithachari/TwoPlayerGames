# Two Player Games
Implementation of chess player using Minimax, Alpha-Beta Pruning and Stochastic Search

## A minimax search
Implemented a minimax search algorithm for a game of Go.
Minimax is a recursive algorithm that searches all possible moves and their outcomes, and then chooses the move that leads to the best possible outcome.
The algorithm was implemented in Python.
The algorithm was tested against a random-move agent and found to be significantly more successful.
The algorithm can be used to improve the performance of any Go game agent.

`python3 main.py --player0 minimax --player1 random`

## Alphabeta Pruning Search
For any given input board, this function should return exactly the same value and moveList as minimax; the only difference between the two functions will be the returned moveTree. The tree returned by alphabeta should have fewer leaf nodes than the one returned by minimax, because alphabeta pruning should make it unnecessary to evaluate some of the leaf nodes.

`python3 main.py --player1 alphabeta`

## Stochastic search
Stochastic search is different from minimax and alphabeta:
1. For every possible initial move, you should evaluate exactly breadth paths, chosen at random using the function chooser.
2. You should compute the values of the leaf nodes for each of these paths.
3. You should then average the path values in order to find the value of the initial move.
4. Finally, among all possible initial moves, find the one that has the best average value ("best" means maximum value if side==False, otherwise it means minimum value). Return its value as value. As moveList, return any list of moves that starts with the optimal move.

`python3 main.py --player1 stochastic`
