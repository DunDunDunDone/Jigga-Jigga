
# Oops! I had row and col backwards throughout all of the code. Mentally replace "row" with "x" and "col" with "y"

########################################################################
##                             RULES OF THE GAME                      ##
########################################################################


## https://docs.google.com/document/d/1KSC47-vuHH_99tvDDdZcIm1gOz1m4oQnFwpVIfQuzIs/edit?usp=sharing

########################################################################
##                               MODULES                              ##
########################################################################

import statistics
import pygame
import random

########################################################################
##                              AI SETUP                              ##
########################################################################

# Import your AI here
from SampleAIs2021 import *
from botvu import *
from Daniel_LaRusso import *
from main import *
from PeterV_RegularAIs import *
from Carl_AI_ import *
from Parley_Aiden import *

BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (240, 0, 0)
GREEN = (0, 240, 0)
YELLOW = (245, 240, 0)
BLUE = (0, 0, 230)

# Add the name of your AI and the function name (just like the sample bots)
name_to_function = {#None: null,
                    'HelterSkelter': HelterSkelter,
                    'IllegalIllia': IllegalIllia,
                    'FourSquare': FourSquare,
                    'EvenSteven': EvenSteven,
                    'OddTodd': OddTodd,
                    'MultipleOfThreeMarie': MultipleOfThreeMarie,
                    'OneEightNate': OneEightNate,
                    'EdgyEddy': EdgyEddy,
                    'botvu 1': bevu,
                    'botvu 2': grevu,
                    'Daniel LaRusso': Daniel_LaRusso,
                    'AlexAi 1': AI1,
                    'AlexAi 2': AI2,
                    'AlexAi 3': AI3,
                    'WebOfGreed': WebOfGreed,
                    'OptimalOwen': OptimalOwen,
                    'BogusBot': BogusBot}

names = [None]*30

# Add your bots name (the same one you used above) to names below
names[0] = 'HelterSkelter'
names[1] = 'IllegalIllia'
names[2] = 'FourSquare'
names[3] = 'OddTodd'
names[4] = 'EvenSteven'
names[5] = 'MultipleOfThreeMarie'
names[6] = 'EdgyEddy'
names[7] = 'OneEightNate'
names[8] = 'botvu 1'
names[9] = 'botvu 2'
names[10] = 'Daniel LaRusso'
names[11] = 'AlexAi 1'
names[12] = 'AlexAi 2'
names[13] = 'AlexAi 3'
names[14] = 'WebOfGreed'
names[15] = 'OptimalOwen'
names[16] = 'BogusBot'


# If you want to run the same match-up multiple times, it may be faster to
#   comment out the input code and just replace it with the numbers you want like so:
#   player_1 = 12#int(input("Enter the number of player 1: "))
#   player_2 = 12#int(input("Enter the number of player 2: "))
#   player_3 = 16#int(input("Enter the number of player 3: "))
#   player_4 = 7#int(input("Enter the number of player 4: "))
player_1 = int(input("Enter the number of player 1: "))
player_2 = int(input("Enter the number of player 2: "))
player_3 = int(input("Enter the number of player 3: "))
player_4 = int(input("Enter the number of player 4: "))

player_names = (names[player_1], names[player_2], names[player_3], names[player_4])
player_functions = (name_to_function[names[player_1]],
                    name_to_function[names[player_2]],
                    name_to_function[names[player_3]],
                    name_to_function[names[player_4]])


########################################################################
##                 FUNCTION DEFINITIONS AND CONSTANTS                 ##
########################################################################


siege_disps = ((-1, 1), (1, -1), (1, 1), (-1, -1)) # Diagonally adjacent squares (for sieges)
decay_disps = ((0, 1), (0, -1), (1, 0), (-1, 0)) # Orthoagonally adjacent squares (for decay)
scoring_disps = ((1, 2), (1, -2), (2, 1), (-2, 1), (-1, 2), (-1, -2), (2, -1), (-2, -1)) # Squares a knight's move away (for scoring)
decay_probabilities = {0: 0, 1: 0.10, 2: 0.14, 3: 0.18, 4: 0.20} # Maps the number of orthoganlly adjecent squares to the probability a square decays

turns_left = 150
points_gained_from_sieges = 1
board_size = 25
corners = ((0, 0), (0, board_size-1), (board_size-1, 0), (board_size-1, board_size-1)) # Coordinates of the four corners of the board
# Yellow: (255, 249, 83), Blue: (13, 249, 253)
colors = {0: (13, 249, 253),
          1: (235, 64, 37), 
          2: (255, 255, 255),  
          3: (235, 64, 37), 
          4: (235, 64, 37),
          5: (255, 255, 255),
          6: (13, 249, 253),
          7: (255, 255, 255),

          8: (145, 92, 224), 
          9: (255, 249, 83), 
          10: (60, 150, 30),
          11: (239, 217, 183),
          12: (180, 136, 102),
          13: (r, g, b),
          #13: (20, 30, 50),
          14: (140, 255, 200),
          15: GRAY,
          16: (163, 2, 34)} # The colors for the different AIs
player_colors  = [(0, 0, 0), colors[player_1], colors[player_2], colors[player_3], colors[player_4]] # The colors that will actually be used in this round


def run_round(board):
    ### Runs a one round of Knight Makes Right
    global turns_left

    random.shuffle(shuffled_player_numbers) # Randomize turn order

    # Goes through the players and runs one turn each
    for num in shuffled_player_numbers:
        move_row, move_col = player_functions[num-1](convert_board(board, num), turns_left, player_previous_moves[num-1])

        # Sets the previous move
        player_previous_moves[num-1] = (move_row, move_col)

        if not inside_board(move_row, move_col) or sum((int(bool(board[move_row+dx][move_col+dy])) for dx, dy in siege_disps if inside_board(move_row+dx, move_col+dy))) >= 3:
            # If your AI makes an illegal move (either plays outside the board or plays into a besiege square), it instead plays at the corner of its starting piece
            move_row, move_col = corners[num-1]
        
        if board[move_row][move_col] == 0:
            # Creates a piece icon in the correct place on
            #   the screen and changes the board state
            create_piece(move_row, move_col, sprites, board, num)

        else: # If it conflicts with with an existing piece (i.e. is a direct attack)
            if random.random() < 0.3: # There's a 0.3 chance of direct attack succeeding

                # Creates a piece icon in the correct place on the screen
                # This overrides the previous image
                create_piece(move_row, move_col, sprites, board, num)

        ### Sieges ###

        captured_squares = []

        # Iterates over all possible sqaures that could be sieged as a result of your move
        for disp in siege_disps:
            
            # These are the coordinates of the square is currently being checked 
            sqaure_x = move_row+disp[0]
            square_y = move_col+disp[1]

            # Checks if there's a piece that is siegable
            if inside_board(sqaure_x, square_y) and not on_the_edge(sqaure_x, square_y) and board[sqaure_x][square_y]:

                surrounding_pieces = [board[sqaure_x+dx][square_y+dy] for dx, dy in siege_disps if board[sqaure_x+dx][square_y+dy]]

                # This is equivalent to the following code that is
                #   commented out below. The code above is faster.
                # surrounding_pieces = []
                # for dx, dy in siege_disps:
                #     if board[row_num+dx][col_num+dy] != 0:
                #         surrounding_pieces.append(board[row_num+dx][col_num+dy])

                if len(surrounding_pieces) >= 3:

                        captured_squares.append((move_row+disp[0], move_col+disp[1]))
                        try:

                            # If one player contributed the most to the siege (i.e. has the most pieces diagonally adjacent to the target)
                            #   they receive points_gained_from_sieges points unless they're sieging their own piece
                            sieger = statistics.mode(surrounding_pieces)
                            if sieger != board[sqaure_x][square_y]:
                                player_capture_points[statistics.mode(surrounding_pieces)-1] += points_gained_from_sieges
                                
                        except statistics.StatisticsError:
                            # A statistics error will occur when two people are tied, in which case neither receive points
                            pass
                            
        # Deletes all the besieged squares
        for row, col in captured_squares:
            # Replaces the current piece with an entirely black image and deletes the piece
            create_piece(row, col, sprites, board, 0)


    ### Decay ###
    
    decayed_squares = []

    # Iterates over all squares in the board to figure out if they will decay
    for row_num, row in enumerate(board):
        for col_num, sqr in enumerate(row):
            if random.random() < decay_probabilities[sum((int(bool(board[row_num+dx][col_num+dy])) for dx, dy in decay_disps if inside_board(row_num+dx, col_num+dy)))]:
                decayed_squares.append((row_num, col_num))

            # This is equivalent to the following code that is commented
            #   out below. The code above is faster.
            # count = 0
            # for dx, dy in decay_disps:
            #     if inside_board(row_num+dx, col_num+dy) and board[row_num+dx][col_num+dy] != 0:
            #         count += 1
            # if random.random() < decay_probabilities[count]:
            #     decayed_squares.append((row_num, col_num))

    # Deletes all the decayed squares
    for row, col in decayed_squares:
        # Replaces the current piece with an entirely black image and deletes the piece
        create_piece(row, col, sprites, board, 0)

    # Resets the connection sprites
    delete_group(connection_sprites)

    ### Knight Scoring Begins ###
    
    # This calculates each player's points from the pieces so it can be displayed during the game
    for i in range(4):
        player_connection_points[i] = 0
    for row_num, row in enumerate(board):
        for col_num, pc in enumerate(row):
            if pc:
                player_connection_points[pc-1] += get_piece_score(board, row_num, col_num, pc)

    # Decrease the turn counter so that the game, you know, ends
    turns_left -= 1

def convert_board(board, player_num):
    ### This function converts the gamestate to match the perspective of the
    ###   player with number player_num (so their pieces will be 1)

    # Ex.
    # Input: 1
    # 1 -> 1
    # 2 -> 2
    # 3 -> 3
    # 4 -> 4

    # Ex.
    # Input: 3
    # 1 -> 3
    # 2 -> 4
    # 3 -> 1
    # 4 -> 2

    return [[(((pc-player_num)%4)+1 if pc else 0) for pc in row] for row in board]

def get_piece_score(board, row, col, player_num):
    ### This returns the score for the piece at row, col and draws lines between connections

    connections = 0
    for dx, dy in scoring_disps:
        if inside_board(row+dx, col+dy):
            if board[row+dx][col+dy] == player_num:
                draw_line(row, col, row+dx, col+dy, player_num, connection_sprites)
                connections += 1
    return connections**3

def inside_board(row, col):
    ### Returns true if the piece is inside the board

    return 0 <= row < len(board) and 0 <= col < len(board)

def on_the_edge(row, col):
    ### Returns true if the piece is on the edge of the board

    return row == len(board)-1 or row == 0 or col == len(board)-1 or col == 0

def draw_line(row_1, col_1, row_2, col_2, player_num, sprite_group):
    ### This creates a line connecting the center of the square row_1, col_1,
    ###   to the center of row_2, col_2. The line will have the color of
    ###   player_num. It alsso gets added to both sprite_group and sprites.

    # Adding 0.5 makes the connection hit the center of the square
    x = (min(row_1, row_2)+0.5)*image_size
    y = (min(col_1, col_2)+0.5)*image_size

    # This figures out 
    if row_1 < row_2:
        x1 = abs(row_2-row_1)*image_size
        x2 = 0
    else:
        x1 = 0
        x2 = abs(row_2-row_1)*image_size

    if col_1 < col_2:
        y1 = abs(col_2-col_1)*image_size
        y2 = 0
    else:
        y1 = 0
        y2 = abs(col_2-col_1)*image_size

    
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface((image_size*(1+abs(col_2-col_1)), image_size*(1+abs(row_2-row_1))))
    sprite.image.set_colorkey((0, 0, 0)) # Makes the background of the sprite transparent
    pygame.draw.line(sprite.image, player_colors[player_num], (x1, y1), (x2, y2), 2)
    
    sprite.rect = sprite.image.get_rect()
    sprite.rect.left = x
    sprite.rect.top = y

    sprite_group.add(sprite)
    sprites.add(sprite)


def update_scores():
    ### Thanks Isaac. Thisaac.
    ### This draws the score bars on the edge of the screen

    import pygame.gfxdraw
    smallfont = pygame.font.SysFont('arial', 30)
    #medfont = pygame.font.SysFont('copperplate', 40)
    #largefont = pygame.font.SysFont('georgia', 60)

    # Removes last round's scoring sprites
    delete_group(scoring_sprites)

    for i in range(4):

        effective_score = player_connection_points[i]+player_capture_points[i]
        # This loop creates multiple score bars
        #   in case the player has a lot of points
        # Each bar has twice as many points as the previous one, 
        #   (so the first bar holds 300 points, the second holds 600, and so on...)

        counter = 0
        while effective_score > 0:
            sprite = pygame.sprite.Sprite()

            # Creates a bar of the appropriate length
            sprite.image = pygame.Surface(((300 if effective_score >= 300*2**counter else effective_score//(2**counter)), 10))
            sprite.image.fill(player_colors[i+1])

            sprite.rect = sprite.image.get_rect()
            sprite.rect.left = 725
            sprite.rect.top = (i+2)*100+counter*15+10

            sprites.add(sprite)
            scoring_sprites.add(sprite)
            
            # Decrements the number of points left to be displayed
            effective_score -= 300*2**counter

            # Keeps track of how many bars have been created
            counter += 1

    # Renders the names of the players
    text = smallfont.render(names[player_1], 1, player_colors[1], (0, 0, 0))
    background.blit(text, (725, 180))
    text = smallfont.render(names[player_2], 1, player_colors[2], (0, 0, 0))
    background.blit(text,(725, 280))
    text = smallfont.render(names[player_3], 1, player_colors[3], (0, 0, 0))
    background.blit(text,(725, 380))
    text = smallfont.render(names[player_4], 1, player_colors[4], (0, 0, 0))
    background.blit(text,(725, 480))

def display_final_scores():
    # Similar to update scores except it only draws the names next to their score as a numeral,
    #   since the bars will already have been drawn

    import pygame.gfxdraw
    smallfont = pygame.font.SysFont('arial', 30)

    effective_scores = [x+y for x, y in zip(player_capture_points, player_connection_points)]

    # Renders the names of the players next to the number of points they scored
    text = smallfont.render(names[player_1]+" "+str(effective_scores[0]), 1, player_colors[1], (0, 0, 0))
    background.blit(text, (725, 180))
    text = smallfont.render(names[player_2]+" "+str(effective_scores[1]), 1, player_colors[2], (0, 0, 0))
    background.blit(text,(725, 280))
    text = smallfont.render(names[player_3]+" "+str(effective_scores[2]), 1, player_colors[3], (0, 0, 0))
    background.blit(text,(725, 380))
    text = smallfont.render(names[player_4]+" "+str(effective_scores[3]), 1, player_colors[4], (0, 0, 0))
    background.blit(text,(725, 480))

    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)

def delete_group(sprite_group):
    # Deletes all sprites in a sprite group

    for sprite in sprite_group:
        sprite.kill()

def create_piece(row, col, sprite_group, board, player_num):
    ### This creates a piece for the player with number player_num in
    ###   board at row, col. It also makes an icon and adds it to sprite_group.

    board[row][col] = player_num
    
    sprite = pygame.sprite.Sprite()
    sprite_group.add(sprite)
    sprite.image = pygame.Surface((image_size, image_size))
    sprite.image.fill(player_colors[player_num])

    # x and y are the position on the screen
    x = row*image_size
    y = col*image_size
    
    sprite.rect = sprite.image.get_rect()
    sprite.rect.left = x
    sprite.rect.top = y

########################################################################
##                      BOARD AND PYGAME WINDOW SETUP                 ##
########################################################################

### Pygame Setup ###

pygame.init()
sprites = pygame.sprite.Group()

width = 1100
height = 700
image_size = 28

closed = False

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Knight Makes Right")
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
screen.blit(background, (0, 0))

sprites = pygame.sprite.Group()
scoring_sprites = pygame.sprite.Group()
connection_sprites = pygame.sprite.Group()

### Player Setup ###

# Current total of points scored by pieces
player_connection_points = [0, 0, 0, 0]

# Cumulative total of points gained from sieges
player_capture_points = [0, 0, 0, 0]

# List of tuples containing each players previous moves
player_previous_moves = [None, None, None, None]

# To randomize turn order, this list is shuffled
# The numbers correspond to the player numbers which
#   are one more than their index in player_functions
shuffled_player_numbers = [1, 2, 3, 4]

### Board Setup ###

# This initializes the board
board = [[0 for i in range(board_size)] for j in range(board_size)] # Inner lists are rows # 0 is empty, 1-4 is the corresponding player


# This gives every player one corner to start out with

for player in range(4):
    player_previous_moves[player] = corners[player]
    create_piece(corners[player][0], corners[player][1], sprites, board, player+1)

########################################################################
##                              MAINLOOP                              ##
########################################################################

update_scores()
pygame.display.update()
clock.tick(30)

while not closed and turns_left > 0:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            closed = True
    run_round(board)
    update_scores()

    # Draws all the graphics on the screen
    screen.blit(background, (0, 0))
    sprites.clear(screen, background)
    sprites.update()
    sprites.draw(screen)
    pygame.display.update()
    clock.tick(8)


########################################################################
##                               SCORES                               ##
########################################################################

print("Scores: ")
for index in range(4):
    print("%s scored %d points." % (player_names[index], round(player_connection_points[index]+player_capture_points[index])))

display_final_scores()

while not closed:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            closed = True

    pygame.display.update()
    clock.tick(100)

pygame.quit()

