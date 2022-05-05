# Tic-Tack-Toe
Two ways to solve Tic Tack Toe


The first method is more of a brute force. Since the game has relatively little outcomes (around 250.000) this is a solid way to always draw or win. 
The algorithm I used is fairly similar to the Minimax algorithm. 
This algorithm wins if it has a forced win, otherwise it will draw. 
Something interesting to note is that it doesn't care when it wins. If it calculates it can win in 3 moves or in 1 move, it will just pick "randomly".


The second method trains a neural network to play the game. 
The entire model was built from scratch. It uses an evolutionary approach to train, instead of a more traditional optimizer.
While this is a fairly primitive way of training a neural network, it still achieved an accuracy of around 95%. In this case that means the AI wins/draws 95% of the games it plays against an opponent which makes random moves.
This accuracy is much higher than the 75% a classmate achieved using NEAT.
