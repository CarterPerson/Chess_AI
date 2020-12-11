import chess

class MinimaxAI():
    def __init__(self, depth, min_or_max):
        self.depth = depth
        self.max_checkmate = 500
        self.mini_checkmate = -500
        self.goal = min_or_max # Boolean, true = white: max player, false = black: min player.
        self.visited = 0

    def mini(self, board, currdepth):
        self.visited = self.visited + 1
        if self.cutoff(board, currdepth)[0]:
            return self.cutoff(board, currdepth)[1]
        mini = 999
        for move in board.legal_moves:
            board.push(move)
            tempmax = self.max(board, currdepth+1)
            if tempmax < mini:
                mini = tempmax
            board.pop()
        return mini


    def max(self, board, currdepth):
        self.visited = self.visited + 1
        if self.cutoff(board, currdepth)[0]:
            return self.cutoff(board, currdepth)[1]
        max = -999
        for move in board.legal_moves:
            board.push(move)
            tempmin = self.mini(board, currdepth+1)
            if tempmin > max:
                max = tempmin
            board.pop()
        return max

    def cutoff(self, board, currdepth):
        if currdepth >= self.depth:
            return (True, self.evaluate(board))
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
        total = total + 600 * len(board.pieces(chess.KING, chess.WHITE))

        # Black pieces
        total = total - len(board.pieces(chess.PAWN, chess.BLACK))
        total = total - 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
        total = total - 5 * len(board.pieces(chess.ROOK, chess.BLACK))
        total = total - 3 * len(board.pieces(chess.KNIGHT, chess.BLACK))
        total = total - 9 * len(board.pieces(chess.QUEEN, chess.BLACK))
        total = total - 600 * len(board.pieces(chess.KING, chess.BLACK))

        return total


    def choose_move(self, board):
        bestmove = None
        self.visited = 0
        analyze = 0
        if self.goal:
            analyze = -999
        if not self.goal:
            analyze = 999
        for move in board.legal_moves:
            board.push(move)
            if self.goal:
                score = self.mini(board, 1)
                if score > analyze:
                    analyze = score
                    bestmove = move
            if not self.goal:
                score = self.max(board, 1)
                if score < analyze:
                    analyze = score
                    bestmove = move
            board.pop()
        print('depth: ' + str(self.depth) + ', states visited: ' + str(self.visited) + ', move: ' + str(bestmove))
        print('Current score: '+ str(analyze))
        return bestmove


