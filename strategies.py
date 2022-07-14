"""
Some example strategies for people who want to create a custom, homemade bot.
And some handy classes to extend
"""

import chess
from chess.engine import PlayResult
import random
from engine_wrapper import EngineWrapper
import re
#import numpy as np
#from tjayada_bot import TjaYaDa


class FillerEngine:
    """
    Not meant to be an actual engine.

    This is only used to provide the property "self.engine"
    in "MinimalEngine" which extends "EngineWrapper"
    """
    def __init__(self, main_engine, name=None):
        self.id = {
            "name": name
        }
        self.name = name
        self.main_engine = main_engine

    def __getattr__(self, method_name):
        main_engine = self.main_engine

        def method(*args, **kwargs):
            nonlocal main_engine
            nonlocal method_name
            return main_engine.notify(method_name, *args, **kwargs)

        return method


class MinimalEngine(EngineWrapper):
    """
    Subclass this to prevent a few random errors

    Even though MinimalEngine extends EngineWrapper,
    you don't have to actually wrap an engine.

    At minimum, just implement `search`,
    however you can also change other methods like
    `notify`, `first_search`, `get_time_control`, etc.
    """
    def __init__(self, commands, options, stderr, draw_or_resign, name=None, **popen_args):
        super().__init__(options, draw_or_resign)

        self.engine_name = self.__class__.__name__ if name is None else name

        self.engine = FillerEngine(self, name=self.name)
        self.engine.id = {
            "name": self.engine_name
        }

    def search(self, board, time_limit, ponder, draw_offered):
        """
        The method to be implemented in your homemade engine

        NOTE: This method must return an instance of "chess.engine.PlayResult"
        """
        raise NotImplementedError("The search method is not implemented")

    def notify(self, method_name, *args, **kwargs):
        """
        The EngineWrapper class sometimes calls methods on "self.engine".
        "self.engine" is a filler property that notifies <self>
        whenever an attribute is called.

        Nothing happens unless the main engine does something.

        Simply put, the following code is equivalent
        self.engine.<method_name>(<*args>, <**kwargs>)
        self.notify(<method_name>, <*args>, <**kwargs>)
        """
        pass


class ExampleEngine(MinimalEngine):
    pass


# Strategy names and ideas from tom7's excellent eloWorld video

def init_evaluate_board(board):
    global boardvalue

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.KING, chess.BLACK)])

    boardvalue = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    return boardvalue


pawntable = [
  0,   0,   0,   0,   0,   0,   0,   0,
 78,  83,  86,  73, 102,  82,  85,  90,
  7,  29,  21,  44,  40,  31,  44,   7,
-17,  16,  -2,  15,  14,   0,  15, -13,
-26,   3,  10,   9,   6,   1,   0, -23,
-22,   9,   5, -11, -10,  -2,   3, -19,
-31,   8,  -7, -37, -36, -14,   3, -31,
  0,   0,   0,   0,   0,   0,   0,   0]

knightstable = [
-66, -53, -75, -75, -10, -55, -58, -70,
 -3,  -6, 100, -36,   4,  62,  -4, -14,
 10,  67,   1,  74,  73,  27,  62,  -2,
 24,  24,  45,  37,  33,  41,  25,  17,
 -1,   5,  31,  21,  22,  35,   2,   0,
-18,  10,  13,  22,  18,  15,  11, -14,
-23, -15,   2,   0,   2,   0, -23, -20,
-74, -23, -26, -24, -19, -35, -22, -69]

bishopstable = [
-59, -78, -82, -76, -23,-107, -37, -50,
-11,  20,  35, -42, -39,  31,   2, -22,
 -9,  39, -32,  41,  52, -10,  28, -14,
 25,  17,  20,  34,  26,  25,  15,  10,
 13,  10,  17,  23,  17,  16,   0,   7,
 14,  25,  24,  15,   8,  25,  20,  15,
 19,  20,  11,   6,   7,   6,  20,  16,
 -7,   2, -15, -12, -14, -15, -10, -10]

rookstable = [
 35,  29,  33,   4,  37,  33,  56,  50,
 55,  29,  56,  67,  55,  62,  34,  60,
 19,  35,  28,  33,  45,  27,  25,  15,
  0,   5,  16,  13,  18,  -4,  -9,  -6,
-28, -35, -16, -21, -13, -29, -46, -30,
-42, -28, -42, -25, -25, -35, -26, -46,
-53, -38, -31, -26, -29, -43, -44, -53,
-30, -24, -18,   5,  -2, -18, -31, -32]

queenstable = [
  6,   1,  -8,-104,  69,  24,  88,  26,
 14,  32,  60, -10,  20,  76,  57,  24,
 -2,  43,  32,  60,  72,  63,  43,   2,
  1, -16,  22,  17,  25,  20, -13,  -6,
-14, -15,  -2,  -5,  -1, -10, -20, -22,
-30,  -6, -13, -11, -16, -11, -16, -27,
-36, -18,   0, -19, -15, -15, -21, -38,
-39, -30, -31, -13, -31, -36, -34, -42]

kingstable = [
  4,  54,  47, -99, -99,  60,  83, -62,
-32,  10,  55,  56,  56,  55,  10,   3,
-62,  12, -57,  44, -67,  28,  37, -31,
-55,  50,  11,  -4, -19,  13,   0, -49,
-55, -43, -52, -28, -51, -47,  -8, -50,
-47, -42, -43, -79, -64, -32, -29, -32,
 -4,   3, -14, -50, -57, -18,  13,   4,
 17,  30,  -3, -14,   6,  -1,  40,  18]


def evaluate_board(board):


    if board.is_checkmate():
        return -9999

    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    eval = init_evaluate_board(board)
    return eval
    #if board.turn:
    #    return eval
    #else:
    #    return -eval



def negaMax( board, depth, alpha, beta, color):

    if ( depth == 0 ):
        return color * evaluate_board(board)

    value = -9999
    moves = list(board.legal_moves)

    for move in moves:
        board.push(move)
        value = max(value, -negaMax(board, depth-1, -beta, -alpha, -color))
        alpha = max(alpha, value)
        board.pop()

        if alpha > beta:
            return value

    return value





def rootNegaMax(board, depth, alpha, beta, color):

    moves = list(board.legal_moves)

    best_move_found = moves[0]
    maxima = -9999

    for move in moves:
        board.push(move)
        value = -negaMax(board, depth-1, -beta, -alpha, -color)
        board.pop()

        if( value > maxima ):
            maxima = value
            best_move_found = move

    return best_move_found



class TjaYaDa(ExampleEngine):
    def search(self, board, *args):
        print("lets start searching")
        # check if white
        global ai_white

        if board.turn:
            ai_white = True
            # open white library
            with open('data/new_lost_clean_white_chess.txt') as f:
                lines = f.readlines()

            possible = []
            possible_sqr = []

            for idx,line in enumerate(lines):
                if line == "\n":
                    possible_sqr.append(possible)
                    possible = []

                elif len(line) > 10:
                    possible.append(line.strip())


            current_move = board.fen()
            current_move = re.sub(r' \d+$', '', current_move)
            current_move = re.sub(r' \d+$', '', current_move)

            what_now = []

            for i in range(len(possible_sqr)):
                if current_move in possible_sqr[i]:
                    for idx, target_move in enumerate(possible_sqr[i]):
                        if target_move == current_move:
                            try:
                                what_now.append(possible_sqr[i][idx+1])
                            except:
                                print("An exception occurred")
                            break

            if len(what_now) > 0:
                our_choice = random.choice(what_now)

                WantedBoard = chess.Board(our_choice)
                move_to_play = TryMove(board, WantedBoard)
                print("data move:", move_to_play)
                return PlayResult(move_to_play, None)



            else:
                move_to_play = rootNegaMax(board, 3, -9999, 9999, 1)
                print("eval move:", move_to_play)
                return PlayResult(move_to_play, None)


        # if ai is black
        else:
            ai_white = False
            # open white library
            with open('data/lost_clean_black_chess.txt') as f:
                lines = f.readlines()

            possible = []
            possible_sqr = []

            for idx,line in enumerate(lines):
                if line == "\n":
                    possible_sqr.append(possible)
                    possible = []

                elif len(line) > 10:
                    possible.append(line.strip())


            current_move = board.fen()
            current_move = re.sub(r' \d+$', '', current_move)
            current_move = re.sub(r' \d+$', '', current_move)

            what_now = []

            for i in range(len(possible_sqr)):
                if current_move in possible_sqr[i]:
                    for idx, target_move in enumerate(possible_sqr[i]):
                        if target_move == current_move:
                            try:
                                what_now.append(possible_sqr[i][idx+1])
                            except:
                                print("An exception occurred")
                            break

            if len(what_now) > 0:
                our_choice = random.choice(what_now)

                WantedBoard = chess.Board(our_choice)
                move_to_play = TryMove(board, WantedBoard)
                print("data move:", move_to_play)
                return PlayResult(move_to_play, None)



            else:
                move_to_play = rootNegaMax(board, 3, -9999, 9999, -1)
                print("eval move:", move_to_play)
                return PlayResult(move_to_play, None)




def TryMove(CurrentBoard, WantedBoard):
    legal_moves = list(CurrentBoard.legal_moves)
    for move in legal_moves:
        TryCurrentBoard = CurrentBoard.copy()
        TryCurrentBoard.push(move)

        TryMove, WantMove = re.sub(r' \d+$', '', TryCurrentBoard.fen()), re.sub(r' \d+$', '', WantedBoard.fen())
        TryMove, WantMove = re.sub(r' \d+$', '', TryMove), re.sub(r' \d+$', '', WantMove)

        if TryMove == WantMove:
            return move

#####################################

class RandomMove(ExampleEngine):
    def search(self, board, *args):
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    def search(self, board, *args):
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Gets the first move when sorted by uci representation"""
    def search(self, board, *args):
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)
