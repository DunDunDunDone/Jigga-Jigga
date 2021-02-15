import random

def HelterSkelter(board, turns_left, previous_move):
    # Plays randomly
    # "I could be playing the perfect game; you never know..."
    return (random.randint(0, 24), random.randint(0, 24))

def IllegalIllia(board, turns_left, previous_move):
    # Only plays the same illegal move over and over again
    # "Lol. Imagine, you know, following the rules..."
    return (-47, 167)

def FourSquare(board, turns_left, previous_move):
    # Plays four cycles.
    # "It's time four unfourgetable cycles. My fources will fourtify and move fourward..."
    # Note: originally coded in Fourtran
    if turns_left%4 == 0 or previous_move == None:
        return (random.randint(0, 24), random.randint(0, 24))
    elif turns_left%4 == 1:
        return (previous_move[0]+1, previous_move[1]-2)
    elif turns_left%4 == 2:
        return (previous_move[0]+2, previous_move[1]+1)
    elif turns_left%4 == 3:
        return (previous_move[0]-1, previous_move[1]+2)

def EvenSteven(board, turns_left, previous_move):
    # Plays on coordinates that are both even
    # "You know who's the worst? Evan Kevin. Literally all those vowels are
    #    pronounced wrong! Kevin doesn't even have an even number of letters...."
    return (random.randint(0,12)*2, random.randint(0,12)*2)

def OddTodd(board, turns_left, previous_move):
    # Starts in the upper left and moves right skipping every other square
    # "Without a doubt it's Tod. Those letters are way nicer; one fewer character makes quite a change."
    if turns_left == 150:
        return (0, 1)
    if previous_move[0] > 22:
        return ((previous_move[0]+2)%25, (previous_move[1]+1)%25)
    else:
        return (previous_move[0]+2, previous_move[1])

def MultipleOfThreeMarie(board, turns_left, previous_move):
    # Only plays on coordinates whose sum is a multiple of three
    # "N times three, leave me be!"
    if previous_move == None:
        return (0, 0)
    else:
        # This sets the candidate for the next move to be three down from the last move
        # It carries if this move would be off the map
        move = (previous_move[0]+(previous_move[1]+3)//25, (previous_move[1]+3)%25)
        while move[0] < 25: # If it's off the map, it breaks out of the loop
            if not board[move[0]][move[1]]: # Only plays in empty squares
                return move
            move = (move[0]+(move[1]+3)//25, (move[1]+3)%25)

    # If it can't find a move, it uses the following code pick randomly
    rand_row = random.randint(0, 24)
    return (rand_row, 3*random.randint(int(rand_row%3 != 0), 8)-(rand_row%3))

def OneEightNate(board, turns_left, previous_move):
    # Tries to get one piece surrounded by 8 other pieces in the center
    # "One eight, that's all I need! I mean, it's worth 512 points after all..."

    for move in ((12, 12), (13, 14), (13, 10), (14, 13), (10, 13), (11, 14), (11, 10), (14, 11), (10, 11)):
        # Checks whether he's played on the sqaure
        if board[move[0]][move[1]] != 1:
            return move
    # If he has all the squares for the knight surrounded by eight other pieces, he plays randomly
    return (random.randint(0, 24), random.randint(0, 24))
    
def EdgyEddy(board, turns_left, previous_move):
    # Tries to play a knight's move away and towards the edge
    # "Stay on the edges, avoid conflict, that's my strategy."

    def inside_board(row, col):
        return 0 <= row < len(board) and 0 <= col < len(board)

    # These moves (relative to previous_move) are ordered so that the first legal move is towards the edge
    moves = {"upper_left": ((-2, -1), (-2, 1), (-1, 2), (1, 2)),
            "upper_right": ((1, -2), (-1, -2), (-2, -1), (-2, 1)),
            "lower_left": ((-1, 2), (1, 2), (2, 1), (2, -1)),
            "lower_right": ((2, 1), (2, -1), (1, -2), (-1, -2))}

    if previous_move[0] < 13:
        if previous_move[1] < 13:
            quadrant = "upper_left"
        else:
            quadrant = "lower_left"
    else:
        if previous_move[1] < 13:
            quadrant = "upper_right"
        else:
            quadrant = "lower_right"

    for disp in moves[quadrant]:
        if inside_board(previous_move[0]+disp[0], previous_move[1]+disp[1]):
            return (previous_move[0]+disp[0], previous_move[1]+disp[1])
