import numpy as np
import random
import pygame
import sys
import math
import tkinter as tk
from tkinter import simpledialog
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)  # Fixed typo in color name
GRAY = (128, 128, 128)  # Updated to gray

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2


# get_board_size(): Prompts the user to enter the desired board size using a GUI and validates the input.
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

# Update the window length for larger board size
WINDOW_LENGTH = min(6, board_size)
# Define the create_board function
def create_board(n):
    board = np.zeros((n, n))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[board.shape[0] - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(board.shape[0]):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check vertical locations for win
    for c in range(board.shape[1]):
        for r in range(board.shape[0] - WINDOW_LENGTH + 1):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check positively sloped diagonals
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(board.shape[0] - WINDOW_LENGTH + 1):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    
    # Check negatively sloped diagonals
    for c in range(board.shape[1] - WINDOW_LENGTH + 1):
        for r in range(WINDOW_LENGTH - 1, board.shape[0]):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0
def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, board.shape[1] // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(board.shape[0]):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(board.shape[1] - WINDOW_LENGTH + 1):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(board.shape[1]):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(board.shape[0] - WINDOW_LENGTH + 1):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonal
    for r in range(board.shape[0] - WINDOW_LENGTH + 1):
        for c in range(board.shape[1] - WINDOW_LENGTH + 1):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonal
    for r in range(board.shape[0] - WINDOW_LENGTH + 1):
        for c in range(board.shape[1] - WINDOW_LENGTH + 1):
            window = [board[r + i][c + WINDOW_LENGTH - 1 - i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score
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
def get_valid_locations(board):
    valid_locations = []
    for col in range(board.shape[1]):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


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
# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True  # Set the game_over flag to exit the loop

#         if event.type == pygame.MOUSEMOTION:
#             pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
#             posx = event.pos[0]
#             if turn == PLAYER:
#                 pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN:
#                 pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx, posy = event.pos
                col = int((posx ) // SQUARESIZE)
                row = int((posy ) // SQUARESIZE)
                num_rows, num_cols = board_size, board_size
                row = num_rows - 1 - row
                print(f"Row: {row}, Column: {col}")

                if is_valid_location(board, col):
                    drop_piece(board, row, col, PLAYER_PIECE)
                    print_board(board)
                    draw_board(board)

                    if winning_move(board, PLAYER_PIECE):
                        print("Player 1 wins!!")
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    elif winning_move(board, AI_PIECE):
                        print("AI wins!!")
                        label = myfont.render("Ai wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    elif len(get_valid_locations(board)) == 0:
                        print("It's a draw!")
                        label = myfont.render("It's a draw!", 1, (255, 255, 255))
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2



    if turn == AI and not game_over:
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            print_board(board)
            draw_board(board)

        if winning_move(board, AI_PIECE):
                label = myfont.render("AI wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
        elif len(get_valid_locations(board)) == 0:
                label = myfont.render("It's a draw!", 1, (255, 255, 255))
                screen.blit(label, (40, 10))
                game_over = True



        turn += 1
        turn = turn % 2
    
    pygame.display.update()

    if game_over:
        pygame.time.delay(2000)  # Increased delay to 3 seconds

# Quit pygame and exit the program
pygame.quit()
sys.exit()