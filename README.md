# Project: Tic-Tac-Toe AI Solvers

## Overview

This project explores two distinct approaches to developing an Artificial Intelligence capable of playing Tic-Tac-Toe optimally or near-optimally. The goal was to implement and compare a traditional game-tree search algorithm with a machine learning-based approach using a neural network trained via evolutionary methods.

## Implemented Approaches

### 1. Minimax-based Solver

This method implements a deterministic algorithm to find the optimal move in any given Tic-Tac-Toe state.

- **Algorithm:** The approach is fundamentally similar to the Minimax algorithm, exploring the game tree to determine the best possible outcome. Given Tic-Tac-Toe's relatively small state space (approximately 250,000 unique states), a brute-force search is computationally feasible.
- **Strategy:** The algorithm guarantees a win if a forced win sequence exists from the current state. Otherwise, it ensures at least a draw against any opponent.
- **Behavior Note:** An interesting characteristic observed is its indifference towards the speed of victory. If multiple paths lead to a win (e.g., winning in 1 move vs. 3 moves), the algorithm does not prioritize the faster win and may select among winning moves arbitrarily.

### 2. Neural Network Solver (Evolutionary Approach)

This method utilizes a neural network, built entirely from scratch, to learn how to play Tic-Tac-Toe.

- **Training Method:** Instead of traditional gradient-based optimizers (like backpropagation), this network was trained using an evolutionary strategy. This involves generating variations of the network and selecting the best performers over generations.
- **Architecture:** _(Consider adding details about the network architecture if available - e.g., number of layers, neurons, activation functions)._
- **Performance:** While evolutionary training can be considered a more primitive approach for neural networks, this model achieved a notable success rate. When evaluated against an opponent making random moves, the AI successfully wins or draws approximately 95% of the games.
- **Comparative Result:** This 95% win/draw rate significantly outperforms the ~75% accuracy achieved by a peer using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm for the same task, demonstrating the effectiveness of this custom implementation.
