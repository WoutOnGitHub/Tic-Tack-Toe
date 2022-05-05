from os import system
from random import choice

swap_turn = {"x":"o",
			 "o":"x"}


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

def get_move(turn, player, board, random):
	temp_board = board.copy()
	if turn == player:
		if random:
			moves = find_possible_moves(board)
			return choice(moves)
		move = input(
			"Which square would you like to fill in? (0-8) If you do not enter a number the program will error out. "
			)
		while int(move) not in range(0,9) or temp_board[int(move)] != " ":
			print("Your move has to be a number between 0 and 8")
			move = input("Which square would you like to fill in? (0-8) ")
		return int(move)
		
	else:
		if is_empty(board):
			return 0
		games_tree = Tree(temp_board, swap_turn[player])
		for child in games_tree.root.children:
			if child.valid == 1:
				return int(child.previous_move)
		for child in games_tree.root.children:
			if child.valid == 0:
				return int(child.previous_move)

def make_move(board, player, move):
	temp_board = board.copy()
	temp_board[move] = player
	return temp_board

def most_common(lst):
    return max(set(lst), key=lst.count)

def clear():
	_ = system('clear')

def create_children(board, turn, player):
	temp_board = board.copy()
	moves = find_possible_moves(temp_board)
	if moves == []:
		return []
	children = []
	for move in moves:
		children.append(TreeNode(make_move(temp_board, turn, move), swap_turn[turn], move, player))
	return children

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

class TreeNode:
	def __init__(self, board, turn, previous_move, player):
		self.board = board.copy()
		self.turn = turn
		self.player = player
		self.children = create_children(self.board, self.turn, self.player)
		self.previous_move = previous_move
		self.state = str(get_state(board))


		if self.state == self.player:
			self.valid = 1
		if self.state == swap_turn[player]:
			self.valid = -1
		if self.state == "drawn":
			self.valid = 0
		if self.state == "not-finished":
			self.valid = self.is_valid()

	def is_valid(self):
		if self.turn == self.player:
			for child in self.children:
				if child.valid == 1:
					return 1
			for child in self.children:
				if child.valid == 0:
					return 0
			else:
				return -1

		if self.turn == swap_turn[self.player]:
			for child in self.children:
				if child.valid == -1:
					return -1
			for child in self.children:
				if child.valid == 0:
					return 0
			else:
				return 1

class Tree:
	def __init__(self, board, player):
		self.root = TreeNode(board, player, None, player)


def play_game(starts):
	player = "x"
	if starts == "random":
		turn = choice(["x","o"])
	elif starts == "you":
		turn = "x"
	else:
		turn = "o"
	board = []
	for _ in range(9):
		board.append(" ")
	while True:
		clear()
		print(f"It's {turn}'s turn")
		print_board(board)
		move = get_move(turn, player, board, False)
		board = make_move(board, turn, move)
		state = get_state(board)
		if state == "drawn":
			clear()
			print_board(board)
			print("It is a draw!")
			break
		if state == "x":
			clear()
			print_board(board)
			print("X won")
			break
		if state == "o":
			clear()
			print_board(board)
			print("o won")
			break
		turn = swap_turn[turn]

def test_game(starts):
	player = "o"
	if starts == "alice":
		turn = "x"
	elif starts == "bob":
		turn = "o"
	else:
		turn = choice(["o", "x"])

	board = []
	for _ in range(9):
		board.append(" ")

	while True:
		move = get_move(turn, player, board, True)
		board = make_move(board, turn, move)
		state = get_state(board)
		if state == "drawn":
			return "drawn"
			break
		if state == "x":
			return "x"
			break
		if state == "o":
			return "o"
			break
		turn = swap_turn[turn]

print("Do you want to play against the computer or would you like to see how it performs against an opponent which only makes random moves?")
play = input("play/view ")
while play not in ["play", "view"]:
	play = input("You can choose between play or view ")

if play == "play":
	print("Who would you like to start?")
	starts = input("you / computer / random ")
	while starts not in ["you", "computer", "random"]:
		starts = input("If you would like to start, type 'you'. If you want the computer to start, type 'computer'. If you want the computer to randomly decide who starts type 'random'")
	play_game(starts)

elif play == "view":
	clear()
	print("You can't view each game as it is being played. This is because that would require the print function to be used. The problem with this is that it is one of the slowest functions in Python and would greatly decrease the speed at which this program would run. The goal of this program is to see how well my algorithm performs.")
	print("Alice is an algorithm programmed by Wout van der Hoef that tries to find the best move possible")
	print("Bob just picks a random square each time it's his turn")
	print("Alice almost never loses if she starts")
	print("Who would you like to start each game")
	starts = input("random / alice / bob ")
	while starts not in ["random", "alice", "bob"]:
		starts = input("You can choose between: random, alice or bob ")

	alice_wins = 0
	bob_wins = 0
	draws = 0
	total_games = 0

	while True:
		result = test_game(starts)
		if result == "x":
			alice_wins += 1
		elif result == "drawn":
			draws += 1
		else:
			bob_wins += 1
		total_games += 1
		clear()
		print(f"Alice wins: {alice_wins}")
		print(f"Bob wins: {bob_wins}")
		print(f"Draws: {draws}")
		print("")
		print(f"Alice win percentage: {alice_wins/total_games * 100}%")
		print(f"Alice draw or win percentage {(alice_wins+draws)/total_games * 100}%")