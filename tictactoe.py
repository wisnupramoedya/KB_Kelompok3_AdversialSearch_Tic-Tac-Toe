import math
import copy

class TicTacToe():
    X = "X"
    O = "O"
    EMPTY = None
    INF_MIN = float("-inf")
    INF_MAX = float("inf")

    def __init__(self):
        super().__init__()
        self.state = [[None, None, None],
            [None, None, None],
            [None, None, None]]
    
    def clear(self):
        self.state = [[None, None, None],
            [None, None, None],
            [None, None, None]]

    def player(self, board):
        """
        Mengembalikan player selanjutnya dalam board
        """

        xCounter = 0
        oCounter = 0

        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == self.X:
                    xCounter += 1
                elif board[i][j] == self.O:
                    oCounter += 1
        
        return self.O if xCounter > oCounter else self.X

    def actions(self, board):
        """
        Mengeluarkan semua action yang mungkin (i, j) pada board
        """
        possibleActions = set()

        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] == self.EMPTY:
                    possibleActions.add((i, j))
        return possibleActions
    
    def result(self, board, action):
        """
        Mengeluarkan hasil dari action (i, j) dalam board
        """
        result = copy.deepcopy(board)
        result[action[0]][action[1]] = self.player(board)
        return result
    
    def winner(self, board):
        """
        Mengembalikan pemenang, jika ada
        """
        # Check rows
        if all(i == board[0][0] for i in board[0]):
            return board[0][0]
        elif all(i == board[1][0] for i in board[1]):
            return board[1][0]
        elif all(i == board[2][0] for i in board[2]):
            return board[2][0]
        # Check columns
        elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
            return board[0][0]
        elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
            return board[0][1]
        elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
            return board[0][2]
        # Check diagonals
        elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
            return board[0][0]
        elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
            return board[0][2]
        else:
            return None

    def terminal(self, board):
        """
        Mengembalikan True jika game selesai, False jika tidak
        """
        if self.winner(board) is not None or (not any(self.EMPTY in sublist for sublist in board) and self.winner(board) is None):
            return True
        else:
            return False

    def utility(self, board):
        """
        Mengembalikan 1 jika X menang, -1 jika O menang, 0 jika seri
        """
        if self.terminal(board):
            winner_side = self.winner(board)
            if winner_side == self.X:
                return 1
            elif winner_side == self.O:
                return -1
            else:
                return 0
    
    def alpha_beta_search(self):
        """
        Mengembalikan action optimal untuk player sekarang
        """
        if self.terminal(self.state):
            return None
        else:
            if self.player(self.state) == self.X:
                value, move = self.max_value(self.state, self.INF_MIN, self.INF_MAX)
                return move
            else:
                value, move = self.min_value(self.state, self.INF_MIN, self.INF_MAX)
                return move
    
    def max_value(self, board, alpha, beta):
        if self.terminal(board):
            return self.utility(board), None
        
        v = self.INF_MIN
        move = None
        for action in self.actions(board):
            v2, action2 = self.min_value(self.result(board, action), alpha, beta)
            if v2 > v:
                v, move = v2, action
                alpha = max(alpha, v)
            
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, board, alpha, beta):
        if self.terminal(board):
            return self.utility(board), None
        
        v = self.INF_MAX
        move = None
        for action in self.actions(board):
            v2, action2 = self.max_value(self.result(board, action), alpha, beta)
            if v2 < v:
                v, move = v2, action
                beta = min(beta, v)
            
            if v <= alpha:
                return v, move
        return v, move