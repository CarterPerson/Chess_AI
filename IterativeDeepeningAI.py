import chess
import time

class IterativeDeepeningAI():
    def __init__(self, depth, min_or_max, length):
        self.depth = depth
        self.max_checkmate = 500
        self.mini_checkmate = -500
        self.goal = min_or_max # Boolean, true = white: max player, false = black: min player.
        self.visited = 0
        self.starttime = None
        self.timelen = length

    def mini(self, board, currdepth, maxdepth, beta = -999):
        self.visited = self.visited + 1
        if self.cutoff(board, currdepth, maxdepth)[0]:
            return self.cutoff(board, currdepth, maxdepth)[1]
        mini = 999
        for move in self.reorder(list(board.legal_moves)):
            board.push(move)
            tempmax = self.max(board, currdepth+1, maxdepth, mini)
            if tempmax < mini:
                mini = tempmax
            board.pop()
            if mini < beta:
                break
        return mini


    def max(self, board, currdepth, maxdepth, alpha = 999):
        self.visited = self.visited + 1
        if self.cutoff(board, currdepth, maxdepth)[0]:
            return self.cutoff(board, currdepth, maxdepth)[1]
        max = -999
        for move in self.reorder(list(board.legal_moves)):
            board.push(move)
            tempmin = self.mini(board, currdepth+1, maxdepth, max)
            if tempmin > max:
                max = tempmin
            board.pop()
            if (max > alpha):
                break
        return max

    def reorder(self, moves):
        return moves
        # return sorted(moves, self.compareStates)

    def compareStates(self, x, y): # This is designed to first look at forward pieces, to "encourage" attacking
        if self.goal:
            return x[-1] - y[-1]
        else:
            return y[-1] - x[-1]


    def cutoff(self, board, currdepth, maxdepth = None):
        if maxdepth is None:
            maxdepth = self.depth
        if currdepth >= maxdepth:
            return (True, self.evaluate(board))
        if time.time() - self.starttime > self.timelen:
            return(True, self.evaluate(board))
        if board.is_checkmate():
            if self.goal:
                return (True, self.mini_checkmate)
            else:
                return (True, self.max_checkmate)
        if board.is_stalemate():
            return (True, 0)
        return (False, None)

    def evaluate(self, board):
        total = 0
        # White pieces
        total = total + len(board.pieces(chess.PAWN, chess.WHITE))
        total = total + 3 * len(board.pieces(chess.BISHOP, chess.WHITE))
        total = total + 5 * len(board.pieces(chess.ROOK, chess.WHITE))
        total = total + 3 * len(board.pieces(chess.KNIGHT, chess.WHITE))
        total = total + 9 * len(board.pieces(chess.QUEEN, chess.WHITE))

        # Black pieces
        total = total - len(board.pieces(chess.PAWN, chess.BLACK))
        total = total - 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
        total = total - 5 * len(board.pieces(chess.ROOK, chess.BLACK))
        total = total - 3 * len(board.pieces(chess.KNIGHT, chess.BLACK))
        total = total - 9 * len(board.pieces(chess.QUEEN, chess.BLACK))

        return total

    def choose_move(self, board):
        self.starttime = time.time()
        self.timelen = self.timelen
        self.visited = 0
        bestmove = None
        depth = 1
        while time.time() - self.starttime < self.timelen:
            oldbest = bestmove
            bestmove = self.find_next(board, depth)
            if(time.time() - self.starttime > self.timelen):
                bestmove = oldbest
            else:
                print('best move for a depth of ' + str(depth) + ' is: ' + str(bestmove))
                depth = depth + 1
        self.starttime = None
        print('depth: ' + str(depth - 1) + ', states visited: ' + str(self.visited) + ', move: ' + str(bestmove))
        return bestmove


    def find_next(self, board, maxdepth = None):
        if maxdepth is None:
            maxdepth = self.depth
        bestmove = None
        analyze = 0
        if self.goal:
            analyze = -999
        if not self.goal:
            analyze = 999
        for move in board.legal_moves:
            board.push(move)
            if self.goal:
                score = self.mini(board, 1, maxdepth)
                if score > analyze:
                    analyze = score
                    bestmove = move
            if not self.goal:
                score = self.max(board, 1, maxdepth)
                if score < analyze:
                    analyze = score
                    bestmove = move
            board.pop()
        return bestmove

