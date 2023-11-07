"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
first_player = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    e = 0
    global first_player
    for i in board:
        for j in i:
            if j == "X":
                x+= 1
            elif j == "O":
                o+= 1
            elif j == None:
                e+=1
                

        
    if first_player == X:
        if e%2 == 0:
            return O
        
        else:
            return X
        
    if first_player == O:
        if e%2 == 0:
            return X
        else:
            return O


def actions(board):

    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves=set()
    for i in range(len(board)):
        
        for j in range(len(board)):
            
            if board[i][j]== None:
                
                moves.add((i,j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[0][i] == board[1][i]== board[2][i] and board[0][i] != None:
            return board[0][i]

        elif board[i][0] == board[i][1] == board[i][2] and  board[i][0] != None:
            return  board[i][0]

    if  board[0][0] ==  board[1][1] ==  board[2][2] and board[0][0] != None:
        return board[0][0]

    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != None:
        return board[0][2]

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    
    for i in board:
        for j in i:
            if j == None:
                return False
    return True




def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None
    
    if player(board) == X:
        aux, m = max_player(board)
        return m
    elif player(board) == O:
        aux, m = min_player(board)
        return m
    
    
def max_player(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    move = None
    for action in actions(board):
        value, act = min_player(result(board, action))
        if value > v:
            v = value
            move = action
            if v == 1:
                return v, move

    return v, move
    
def min_player(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    move  = None
    for action in actions(board):
        value, act = max_player(result(board, action))
        if value < v:
            v = value
            move = action

            if v == -1:
                return v, move

    return v, move
