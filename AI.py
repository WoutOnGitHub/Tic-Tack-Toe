from os import system
from random import choice, randint, random, uniform
from math import e

swap_turn = {"x":"o",
			 "o":"x"}

class NeuralNetwork:
	def __init__(self):
		self.layers = []

	def relu(self, data):
		return max(data,0)

	def soft_max(self, data):
		result = []
		exp_sum_data = 0

		for var in data:
			exp_sum_data += e**var

		for var in data:
			result.append((e**var)/exp_sum_data)

		return result


	def add_layer(self, input_size, output_size):
		layer = []
		for _ in range(output_size):
			layer.append(Node(input_size))
		self.layers.append(layer)

	def input_layer_pass(self,data):
		return data

	def dense_layer_pass(self, data, layer_id):
		result = []
		for node in self.layers[layer_id]:
			output_node = node.bias
			for weight, partial_input in zip(data, node.weights):
				output_node += weight * partial_input
			result.append(self.relu(output_node))
		return result

	def forward_pass(self, data):
		for i in range(len(self.layers)):
			if i == 0:
				data = self.input_layer_pass(data)
			else:
				data = self.dense_layer_pass(data,i)
		return self.soft_max(data)

class Node:
	def __init__(self, input_size):
		self.weights = []
		for _ in range(input_size):
			self.weights.append(uniform(-1,1))
		self.bias = random()

def is_empty(board):
	for i in board:
		if i != " ":
			return False
	return True

def print_board(board):
	space = " " * 10
	print(f'+---+---+---+{space}+---+---+---+')
	print(f'| {board[0]} | {board[1]} | {board[2]} |{space}| 0 | 1 | 2 |')
	print(f'+---+---+---+{space}+---+---+---+')
	print(f'| {board[3]} | {board[4]} | {board[5]} |{space}| 3 | 4 | 5 |')
	print(f'+---+---+---+{space}+---+---+---+')
	print(f'| {board[6]} | {board[7]} | {board[8]} |{space}| 6 | 7 | 8 |')
	print(f'+---+---+---+{space}+---+---+---+')

def get_move(turn, player, board, network):
	temp_board = board.copy()
	if turn == player:
		moves = find_possible_moves(board)
		return choice(moves)
	else:
		temp_board = []
		for i in board:
			if i == " ":
				temp_board.append(0)
			elif i == turn and i != player:
				temp_board.append(-1)
			else:
				temp_board.append(1)

		predictions = network.forward_pass(temp_board)
		possible_moves = find_possible_moves(board)
		possible_predictions = []
		for i in possible_moves:
			possible_predictions.append(predictions[i])


		prediction = max(possible_predictions)
		return predictions.index(prediction)

def make_move(board, player, move):
	temp_board = board.copy()
	temp_board[move] = player
	return temp_board

def clear():
	_ = system('clear')

def find_possible_moves(board):
	moves = []
	for i in range(9):
		if board[i] == " ":
			moves.append(i)
	return moves

def get_state(board):
	for i in range(3):
		if board[i] == board[i+3] and board[i] == board[i+6] and board[i] != " ":
			return board[i]

	for i in [0,3,6]:
		if board[i] == board[i+1] and board[i] == board[i+2] and board[i] != " ":
			return board[i]

	if board[0] == board[4] and board[0] == board[8] and board[0] != " ":
		return board[0]

	if board[2] == board[4] and board[2] == board[6] and board[2] != " ":
		return board[2]

	if " " not in board:
		return "drawn"

	return "not-finished"

def test_game(network):
	player = "o"
	turn = "x"

	board = []
	for _ in range(9):
		board.append(" ")

	while True:
		move = get_move(turn, player, board, network)
		board = make_move(board, turn, move)
		state = get_state(board)
		if state == "drawn":
			return 0
		elif state == "x":
			return 1
		elif state == "o":
			return -1
		turn = swap_turn[turn]

def evaluate_network(network):
	individual_score = 0
	for _ in range(games_per_epoch):
		individual_score += test_game(network)
	return individual_score

def create_offspring(network, learning_rate):
	for layer_i in range(len(network.layers)):
		for node_i in range(len(network.layers[layer_i])):
			for weight_i in range(len(network.layers[layer_i][node_i].weights)):
				num = randint(0,1)
				if num == 1:
					network.layers[layer_i][node_i].weights[weight_i] += learning_rate
				else:
					network.layers[layer_i][node_i].weights[weight_i] -= learning_rate
	return network

def new_gen(scores, networks, learning_rate):
	next_gen = []
	i = 0
	min_score = games_per_epoch
	while len(next_gen) < gen_size:
		if scores[i] == min_score:
			next_gen.append(create_offspring(networks[i], learning_rate))
		i += 1
		if i > gen_size-1:
			i = 0
			#min_score -= 1
	return next_gen

def epoch(networks, learning_rate):
	scores = []
	for network in networks:
		scores.append(evaluate_network(network))
	networks = new_gen(scores, networks, learning_rate)
	return networks, scores

gen_size = 512
learning_rate = 1e-4
learning_decay = 1e-6
networks = []
scores = []
games_per_epoch = 3

for _ in range(gen_size):
	network = NeuralNetwork()
	network.add_layer(9,16)
	network.add_layer(16,16)
	network.add_layer(16,16)
	network.add_layer(16,9)
	networks.append(network)
epoch_i = 0

while learning_rate > 0:
	networks, scores = epoch(networks, learning_rate)
	learning_rate -= learning_decay

	clear()
	wins = 0
	losses = 0
	draws = scores.count(0)
	for i in range(games_per_epoch):
		wins += scores.count(i+1)
		losses += scores.count(-1*(i+1))

	print(f"Win %: {wins/len(scores)*100}")
	print(f"Draw %: {draws/len(scores)*100}")
	print(f"Loss %: {losses/len(scores)*100}")
	print(f"Epochs: {epoch_i}")
	epoch_i += 1








