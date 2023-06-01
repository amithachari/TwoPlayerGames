import math
import chess.lib
from chess.lib.utils import encode, decode
from chess.lib.heuristics import evaluate
from chess.lib.core import makeMove

###########################################################################################
# Utility function: Determine all the legal moves available for the side.
# This is modified from chess.lib.core.legalMoves:
#  each move has a third element specifying whether the move ends in pawn promotion
def generateMoves(side, board, flags):
    for piece in board[side]:
        fro = piece[:2]
        for to in chess.lib.availableMoves(side, board, piece, flags):
            promote = chess.lib.getPromote(None, side, board, fro, to, single=True)
            yield [fro, to, promote]
            
###########################################################################################
# Example of a move-generating function:
# Randomly choose a move.
def random(side, board, flags, chooser):
    '''
    Return a random move, resulting board, and value of the resulting board.
    Return: (value, moveList, boardList)
      value (int or float): value of the board after making the chosen move
      moveList (list): list with one element, the chosen move
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      chooser: a function similar to random.choice, but during autograding, might not be random.
    '''
    moves = [ move for move in generateMoves(side, board, flags) ]
    if len(moves) > 0:
        move = chooser(moves)
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        value = evaluate(newboard)
        print({ encode(*move): {} })
        return (value, [ move ], { encode(*move): {} })
    else:
        return (evaluate(board), [], {})

###########################################################################################
# Stuff you need to write:
# Move-generating functions using minimax, alphabeta, and stochastic search.

def minimax(side, board, flags, depth):
    moveTree = {}
    if depth == 0:
        return (evaluate(board), [], moveTree)
    else:
        if side is True:
            value = math.inf
            bestMove = None
            moveList = []
            moves = [move for move in generateMoves(side, board, flags)]
            for move in moves:
                newside, newboard, newflags = makeMove(True, board, move[0], move[1], flags, move[2])
                moveTree[encode(*move)] = minimax(newside, newboard, newflags, depth - 1)[2]
                if value > minimax(newside, newboard, newflags, depth - 1)[0]:
                    value = minimax(newside, newboard, newflags, depth - 1)[0]
                    bestMove = encode(*move)
                    moveList = minimax(newside, newboard, newflags, depth - 1)[1]
            return (value, [decode(bestMove), *moveList], moveTree)

        else:
            value = -math.inf
            bestMove = None
            moveList = []
            moves = [move for move in generateMoves(side, board, flags)]
            for move in moves:
                newside, newboard, newflags = makeMove(False, board, move[0], move[1], flags, move[2])
                moveTree[encode(*move)] = minimax(newside, newboard, newflags, depth - 1)[2]
                if value < minimax(newside, newboard, newflags, depth - 1)[0]:
                    value = minimax(newside, newboard, newflags, depth - 1)[0]
                    bestMove = encode(*move)
                    moveList = minimax(newside, newboard, newflags, depth - 1)[1]
            return (value, [decode(bestMove), *moveList], moveTree)


def alphabeta(side, board, flags, depth, alpha=-math.inf, beta=math.inf):
    '''
    Return minimax-optimal move sequence, and a tree that exhibits alphabeta pruning.
    Return: (value, moveList, moveTree)
      value (float): value of the final board in the minimax-optimal move sequence
      moveList (list): the minimax-optimal move sequence, as a list of moves
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
    '''
    # raise NotImplementedError("you need to write this!")
    moveList = []
    moveTree = {}
    if depth == 0 or not (generateMoves(side, board, flags)):
        return (evaluate(board), [], moveTree)
    if side is True:
        value = math.inf
        bestMove = None
        moves = [move for move in generateMoves(side, board, flags)]
        for move in moves:
            newside, newboard, newflags = makeMove(True, board, move[0], move[1], flags, move[2])
            moveTree[encode(*move)] = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[2]
            if value > alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[0]:
                value = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[0]
                bestMove = encode(*move)
                moveList = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[1]
            beta = min(beta, value)
            if value <= alpha:
                break
        return (value, [decode(bestMove), *moveList], moveTree)
    else:
        value = -math.inf
        bestMove = None
        for move in generateMoves(side, board, flags):
            newside, newboard, newflags = makeMove(False, board, move[0], move[1], flags, move[2])
            moveTree[encode(*move)] = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[2]
            if value < alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[0]:
                value = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[0]
                bestMove = encode(*move)
                moveList = alphabeta(newside, newboard, newflags, depth - 1, alpha, beta)[1]
            alpha = max(alpha, value)
            if value >= beta:
                break
        return (value, [decode(bestMove), *moveList], moveTree)

def stochastic(side, board, flags, depth, breadth, chooser):
    '''
    Choose the best move based on breadth randomly chosen paths per move, of length depth-1.
    Return: (value, moveList, moveTree)
      value (float): average board value of the paths for the best-scoring move
      moveLists (list): any sequence of moves, of length depth, starting with the best move
      moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
    Input:
      side (boolean): True if player1 (Min) plays next, otherwise False
      board (2-tuple of lists): current board layout, used by generateMoves and makeMove
      flags (list of flags): list of flags, used by generateMoves and makeMove
      depth (int >=0): depth of the search (number of moves)
      breadth: number of different paths
      chooser: a function similar to random.choice, but during autograding, might not be random.
    '''
    # raise NotImplementedError("you need to write this!")
    moveLists = []
    moveTree = {}

    if side:
        best_val = math.inf
    else:
        best_val = -math.inf

    for move in generateMoves(side, board, flags):
        moveList = []
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        moves = [move for move in generateMoves(newside, newboard, newflags)]
        values = []

        moveTree_sub = {}
        for i in range(breadth):
            subMove = chooser(moves)
            newside_submove, newboard_submove, newflags_submove = makeMove(newside, newboard, subMove[0], subMove[1], newflags, subMove[2])
            value, moveList, helperMoveTree = stochastic_helper(newside_submove, newboard_submove, newflags_submove, depth - 2, chooser)
            moveList = [move, subMove, moveList]
            values.append(value)
            moveTree_sub[encode(*subMove)] = helperMoveTree
        moveTree[encode(*move)] = moveTree_sub

        mean_val = sum(values)/len(values)
        prev_val = best_val
        if side:
            best_val = min(mean_val, best_val)
        else:
            best_val = max(mean_val, best_val)

        if prev_val != best_val:
            moveLists = moveList
    return best_val, moveLists, moveTree

def stochastic_helper(side, board, flags, depth, chooser):
    moveList = []
    moveTree = {}
    if depth == 0:
        value = evaluate(board)
    else:
        moves = [move for move in generateMoves(side, board, flags)]
        move = chooser(moves)
        newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
        newValue, newMoveList, newMoveTree = stochastic_helper(newside, newboard, newflags, depth - 1, chooser)
        value = newValue
        moveTree[encode(*move)] = newMoveTree
        moveList = [move, newMoveList]

    return value, moveList, moveTree