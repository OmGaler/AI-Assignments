import copy
import numpy as np
import random
from termcolor import colored  # can be taken out if you don't like it...

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = colored('X', 'red')  # RED_CHAR = 'X'
BLUE_CHAR = colored('O', 'blue')  # BLUE_CHAR = 'O'

EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board():
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip):
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip


def is_valid_location(board, col):
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace("1", RED_CHAR).replace("2", BLUE_CHAR).replace("\n", "|\n") + "|")

def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :]))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c]))):
            return True
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def MoveRandom(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(valid_locations)  
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

def makeMove(board, col, colour): #place a chip into column col, and let gravity take it to its resting place 
    row = get_next_open_row(board, col)
    drop_chip(board, row, col, colour)
    return board

def evaluate(board, chip): #evaluate the state of the board at present, the more positive the number, the better 
    #the situation is for red, the more negative the better it is for blue
    #if the agent is blue, it wants to minimise the numerical value of this function as much as possible in the 
    #minimax tree and assume that the player will choose the best move that maximises the value
    score = 0 #initialise score to zero
    #check to see if there's four in a row - this is a game ender so give it a numerically infinite value so that
    #the minimax algorithm will always prioritise winning and blocking the opponent from winning over every other move, 
    #however good that move is 
    otherChip = RED_INT if chip == BLUE_INT else BLUE_INT
    if game_is_won(board, chip): 
        #game is won, so cannot be a better outcome, return positive infinity if red, negative infinity if blue
        return float("inf") if chip == RED_INT else -float("inf")
    if game_is_won(board, otherChip): #other player wins
        return -float("inf") if chip == RED_INT else float("inf")
    #check to see if there's three in a row with one empty space - high chance of this leading to 
    #four in a row so score it with a relatively large magnitude 
    seq = np.array([chip, chip, chip, 0])
    otherSeq = np.array([otherChip, otherChip, otherChip, 0])
    # Check horizontal sequences, for each three chip sequence of this player's chips, add 10 to the score
    #for each three chip sequence of opponents chips, subtract 10 
    for r in range(ROW_COUNT):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board[r, :]))):
           score += 10 
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board[:, c]))):
            score += 10
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board.diagonal(offset)))):
            score += 10
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, seq))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            score += 10
    #opponents pieces
    for r in range(ROW_COUNT):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board[r, :]))):
           score -= 10 
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board[:, c]))):
            score -= 10
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board.diagonal(offset)))):
            score -= 10
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            score -= 10
    #check sequences of two chips with two empty spaces - more ideal than not having two in a rows, but not as 
    #exciting as three in a row so we'll give it a 2 - just enough to give these positions a slight advantage when 
    #being evaluated for viability
    seq = np.array([chip, chip, 0, 0])
    otherSeq = np.array([otherChip, otherChip, 0, 0])
    # Check horizontal sequences, for each three chip sequence of this player's chips, add 10 to the score
    #for each three chip sequence of opponents chips, subtract 10 
    for r in range(ROW_COUNT):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board[r, :]))):
           score += 2
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board[:, c]))):
            score += 2
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, seq))) in "".join(list(map(str, board.diagonal(offset)))):
            score += 2
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, seq))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            score += 2
    #opponents pieces
    for r in range(ROW_COUNT):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board[r, :]))):
           score -= 2
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board[:, c]))):
            score -= 2
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, board.diagonal(offset)))):
            score -= 2
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, otherSeq))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            score -= 2    
    return score

#construct and traverse a minmax game tree to select the best possible move for our player 
def mm(colour, aleph, bet, d, board): 
    if d == 0: #depth == 0, so stop traversing tree so we can make our way back up and determine which subtree gives the best score
        #so we know to select that move when min/maxing the score
        score = evaluate(board, RED_CHAR if colour == RED_INT else BLUE_CHAR)
        return score, None #return the scoring of this game position which we'll use further up the tree 
        #to decide which moves to take and which to disregard
        #NB the second element in the return tuple is for the move to make, but this is only used when we actually
        #decide on a move (once we reach the top of the tree after our traversal), so we'll leave it as none for now 
    elif game_is_won(board, BLUE_INT) or game_is_won(board, RED_INT):
        if game_is_won(board, BLUE_INT):
            return float("-inf"), None #the best possible outcome for blue, who wants to minimise their score so return the most 
            #negative value possible - no move can top this one 
        if game_is_won(board, RED_INT):
            return float("inf"), None #ditto for red but red is maximising so their best move will be +infinity
    elif len(get_valid_locations(board)) == 0: #no moves left to make, draw and score is zero for both players 
        return 0, None
    else: #haven't reached bottom of tree/ tree still has leaves so continue traversal
        moves = get_valid_locations(board) #all possible moves that can be made at this time, 1 <= moves <= 7
        # if len(moves) > 0: #there are moves available
        move = random.choice(moves) #choose a random move to make, this will likely be replaced with a better move, but for now choose at least one sto start from 
        # else:
            # pass #no moves available, draw, so exit
        score = float("-inf") if colour == RED_INT else float("inf") #initialise score to the worst possible value for this player 
        #because any move is better than not making a move at all (probably)
        for potentialMove in moves: #loop through all moves that can be made and explore the subtrees that they present
            # d-=1 #decrement depth, else a StackOverflow awaits
            newBoard = board.copy() #make a copy of the board for simulation purposes -- saves us having to remove all the chips we place at the end
            makeMove(newBoard, potentialMove, colour) #try this potential move on our 'dummy' board and call the func recursively to see where it leads us
            #get the new score after having made this move, remembering to pass in our alpha/beta values so we can
            #prune unimportant subtrees 
            minimaxscore = mm(RED_INT if colour == BLUE_INT else BLUE_INT, aleph, bet, d-1, newBoard)[0] 
            if colour == RED_INT: #maximising score
                if minimaxscore > score: #new max - better than we've seen so far so we'll select this move and update the score accordingly
                    score = minimaxscore
                    move = potentialMove
                if score > aleph: #update our alpha/beta values for pruning purposes
                    aleph = score
                if aleph >= bet: #alpha/beta pruning: this subtree will yield no better results than we've seen already,
                    #so stop exploring this subtree and move on to save time 
                    break
            elif colour == BLUE_INT: #minimising score
                if minimaxscore < score: #new min, as above 
                    score = minimaxscore 
                    move = potentialMove
                if score < bet: #as above for beta, but this time we're interested in scores less than beta
                    bet = score 
                if bet <= aleph:
                    break #prune
        return score, move #we've reached the end, so return the score and the (hopefully) best move to make 

def agent1move(board):
    valid_locations = get_valid_locations(board)
    return random.choice(valid_locations)

def agent2move(board):
    #find the best move to make through a minimax algorithm
    #get the column that corresponds to the best move we can make
    col = mm(BLUE_INT, float("-inf"), float("inf"), 3, board)[1] #run the algorithm with a search depth of 4 so we can look ahead a little 
    return col


# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
blueWins = 0
redWins = 0
ties = 0
for i in range(100):

    turn = 0

    board = create_board()
    print_board(board)
    game_over = False

    while not game_over:
        if turn % 2 == 0:
            col = agent1move(board) #move randomly
            # col = int(input("RED please choose a column(1-7): "))
            # while col > 7 or col < 1:
            #     col = int(input("Invalid column, pick a valid one: "))
            # while not is_valid_location(board, col - 1):
            #     col = int(input("Column is full. pick another one..."))
            # col -= 1
            row = get_next_open_row(board, col)
            drop_chip(board, row, col, RED_INT)
            # MoveRandom(board,BLUE_INT)

        if turn % 2 == 1 and not game_over:
            # MoveRandom(board,BLUE_INT)
            column=agent2move(board)
            row = get_next_open_row(board, column)
            drop_chip(board, row, column, BLUE_INT)

        print_board(board)
        
        if game_is_won(board, RED_INT):
            redWins += 1
            game_over = True
            print(colored("Red wins!", 'red'))
        if game_is_won(board, BLUE_INT):
            blueWins += 1
            game_over = True
            print(colored("Blue wins!", 'blue'))
        if len(get_valid_locations(board)) == 0:
            ties += 1
            game_over = True
            print(colored("Draw!", 'blue'))
        turn += 1

print("\nWins:")
print("Blue:\t%s" % str(blueWins))
print("Red:\t%s" % str(redWins))

#Output, search depth=3
# Wins:
# Blue:   99
# Red:    1