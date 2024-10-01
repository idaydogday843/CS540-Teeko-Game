import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, drop=True):
        successors = []
        if drop:
            for r in range(5):
                for c in range(5):
                    if state[r][c] == ' ':
                        new_state = [row[:] for row in state]
                        new_state[r][c] = self.my_piece
                        successors.append((new_state, ((r, c),)))
        else:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for r in range(5):
                for c in range(5):
                    if state[r][c] == self.my_piece:
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 5 and 0 <= nc < 5 and state[nr][nc] == ' ':
                                new_state = [row[:] for row in state]
                                new_state[nr][nc] = self.my_piece
                                new_state[r][c] = ' '
                                successors.append((new_state, ((nr, nc), (r, c))))
        return successors


    def game_alg(self, state):
        terminal_val = self.game_value(state)
        if terminal_val != 0:
            return terminal_val

        my_max, opp_max = 0, 0
        lines = []

        for i in range(5):
            horizontal_line = state[i]
            vertical_line = [state[x][i] for x in range(5)]
            lines.append(horizontal_line)
            lines.append(vertical_line)

        diagonals = [
            [state[i][i] for i in range(5)],
            [state[i][4-i] for i in range(5)]
        ]
        lines.extend(diagonals)

        for i in range(4):
            for j in range(4):
                square = [state[i][j], state[i+1][j], state[i][j+1], state[i+1][j+1]]
                lines.append(square)

        for line in lines:
            my_count = line.count(self.my_piece)
            opp_count = line.count(self.opp)
            if ' ' in line:
                my_max = max(my_max, my_count)
                opp_max = max(opp_max, opp_count)

        val = (my_max - opp_max) / 4
        return val


    def max_value(self, state, depth, alpha, beta):
        if depth == 0 or self.game_value(state) != 0:
            return self.game_alg(state)

        v = float('-inf')
        for new_state, _ in self.succ(state, drop=(depth > 3)):
            v = max(v, self.min_value(new_state, depth + 1, alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return v

    def min_value(self, state, depth, alpha, beta):
        if depth == 0 or self.game_value(state) != 0:
            return self.game_alg(state)

        v = float('inf')
        for new_state, _ in self.succ(state, drop=(depth > 3)):
            v = min(v, self.max_value(new_state, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v

    
    def make_move(self, state):
        count = sum(row.count(x) for row in state for x in ['b', 'r'])
        drop_phase = count < 8

        util = {}
        temp_state = copy.deepcopy(state)
        if drop_phase:
            for succ, piece in self.succ(temp_state, drop=True):
                piece_key = tuple(piece[0])  # Ensure the key is immutable
                util[piece_key] = self.max_value(succ, 0, -float("inf"), float("inf"))
            move = [max(util, key=util.get)]
            return move
        else:
            for succ, piece in self.succ(temp_state, drop=False):
                piece_key = tuple(map(tuple, piece))  # Convert list of lists to tuple of tuples
                util[piece_key] = self.max_value(succ, 0, -float("inf"), float("inf"))
            best_move = max(util, key=util.get)
            return list(best_move)


    def opponent_move(self, move):
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    if state[i][j] == self.my_piece:
                        return 1
                    else:
                        return -1
                    
        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(3, 5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    if state[i][j] == self.my_piece:
                        return 1
                    else:
                        return -1

        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row][col+1] == state[row+1][col+1]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1
        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
