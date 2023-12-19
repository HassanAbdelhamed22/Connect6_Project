import numpy as np
import pygame
import sys
import math
import random
import tkinter as tk
from tkinter import simpledialog

ROW_COUNT = 19
COLUMN_COUNT = 19
PLAYER = 0
AI = 1
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 6
# Updated colors
BLUE = (0, 128, 255)  # Updated to a shade of blue
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Updated to red
YELLOW = (255, 255, 0)  # Updated to yellow
GREEN = (0, 255, 0)  # Updated to green
PURPLE = (128, 0, 128)  # Updated to purple
WHITE = (255, 255, 255)  # Fixed typo in color name
GRAY = (128, 128, 128)  # Updated to gray


SQUARESIZE = 40
RADIUS = int(SQUARESIZE / 2 - 2)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

pygame.init()
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 30)

def get_board_size():
    while True:
        try:
            board_size = simpledialog.askinteger("Board Size", "Enter the desired board size (n):")
            if board_size is None:
                # User pressed Cancel
                print("Board size input canceled. Exiting.")
                exit()
            if board_size < 6:
                print("Board size must be at least 6. Please enter a valid size.")
            else:
                return board_size
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Get user input for the board size using GUI
board_size = get_board_size()

# Update the window length for a larger board size
WINDOW_LENGTH = min(6, board_size)


# Define the create_board function
def create_board(n):
    board = np.zeros((n, n))
    return board


'''
    drop_piece(board, row, col, piece): Places a game piece on the game board at the specified row and column.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - row (int): The row where the piece will be placed.
    - col (int): The column where the piece will be placed.
    - piece (int): The identifier for the player or AI piece (e.g., PLAYER_PIECE or AI_PIECE).

    Returns:
    - None: The function modifies the game board in-place.
'''
def drop_piece(board, row, col, piece):
    board[row][col] = piece



'''
    Function:
    - is_valid_location(board, col): Checks if the specified column is a valid location for placing a game piece.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - col (int): The column to be checked for validity.

    Returns:
    - bool: True if the location is valid (empty in the bottom row), False otherwise.

'''
def is_valid_location(board, col):
    return board[board.shape[0] - 1][col] == 0


'''
    Function:
    - get_next_open_row(board, col): Finds the next available row in the specified column.

    Parameters:
    - board (numpy.ndarray): The Connect Four game board.
    - col (int): The column for which to find the next available row.

    Returns:
    - int: The row index of the next available (empty) row in the specified column.
'''
def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r

'''
    Function:
    - print_board(board): Prints the Connect Six game board with the bottom row at the top for better readability.

    Parameters:
    - board (numpy.ndarray): The Connect Six game board.

    Returns:
    - None: The function prints the board to the console.
'''
def print_board(board):
    print(np.flip(board, 0))


def draw_board(board):
    # Fill the entire screen with white color
    screen.fill(WHITE)

    # Dynamically adjust square size based on the board size
    square_size = int(min(SQUARESIZE - 5, height / board.shape[0]))

    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            pygame.draw.rect(screen, GRAY, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE), 5)

    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), square_size // 2)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), square_size // 2)

    pygame.display.update()
    
# Create the game board
board = create_board(board_size)

# Initialize the game state
game_over = False

# Print the initial board
print_board(board)

# Initialize pygame
pygame.init()

# Set the size of each square on the board
SQUARESIZE = min(800 // board_size, 100)

# Set the width and height of the board based on the size of the board
width = (board.shape[1] + 1) * SQUARESIZE
height = (board.shape[1] + 1) * SQUARESIZE

# Dynamically adjust window size based on the board size
if board_size > 6:
    width = min(width, 800)
    height = min(height, 800)

size = (width, height)

# Set the radius of each game piece
RADIUS = int(SQUARESIZE / 2 - 5)

# Create the game window
screen = pygame.display.set_mode(size)

# Draw the initial board
draw_board(board)

# Update the display
pygame.display.update()

# Set the font for displaying messages
myfont = pygame.font.SysFont("monospace", 75)

# Determine the starting player
turn = random.randint(PLAYER, AI)


def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
          #  print (r,col)
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT):
            # Check horizontal
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            # Check vertical
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True

    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            # Check positive diagonal
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
            # Check negative diagonal
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True

    return False

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 6:
     score+=100      
    elif window.count(piece) == 5 and window.count(EMPTY) == 1:
     score += 10
    elif window.count(piece) == 4 and window.count(EMPTY) == 2:
        score += 7
    elif window.count(piece) == 3 and window.count(EMPTY) == 3:
        score += 5
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 3:
        score -= 200
    if window.count(opp_piece) == 4 and window.count(EMPTY) == 2:
        score -= 500
    if window.count(opp_piece) == 5 and window.count(EMPTY) == 1:
        score -= 1000

    return score

def score_position(board, piece):
    score = 0

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r + WINDOW_LENGTH - 1 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score
def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def alpha_beta_pruning(board, depth, alpha, beta, maximizingPlayer, player_turn):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 100000000000000
            elif winning_move(board, PLAYER_PIECE):
                return None, -10000000000000
            else:  # Game is over, no more valid moves
                return None, 0
        else:  # Depth is zero
            if player_turn:  # Player's turn
                return None, score_position(board, PLAYER_PIECE)
            else:  # AI's turn
                return None, score_position(board, AI_PIECE)

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, False, player_turn)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alpha_beta_pruning(b_copy, depth - 1, alpha, beta, True, player_turn)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Player's move
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    draw_board(board)
                    label = myfont.render("Player wins!!", 1, (255, 0, 0))
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    sys.exit()

                draw_board(board)

                # AI's move
                col, _ = minimax(board, depth=1, alpha=-math.inf, beta=math.inf, maximizingPlayer=False)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    draw_board(board)
                    label = myfont.render("AI wins!!", 1, (255, 255, 0))
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                   
                draw_board(board)
                pygame.display.update()
