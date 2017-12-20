import random
import copy
import math


class ConnectFourPlayer:
    def get_move(self):
        # Must return a value between 0 and 6 (inclusive), where 0 is the left-most column and 6 is the right-most column.
        raise NotImplementedError('Must be implemented by subclass')

    def is_automated(self):
        # AI players should return True, human players should return False
        return True


class ConnectFourHumanPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def is_automated(self):
        return False

    def get_move(self):
        valid_input = False
        valid_columns = self.model.get_valid_moves()

        while not valid_input:
            try:
                column = int(input('Enter column (1-7): '))
                if column < 1 or column > 7:
                    raise ValueError()
                else:
                    valid_input = True

                if valid_columns[column-1]:
                    return column-1
                else:
                    print('That column is full. Pick again.')
                    valid_input = False
            except ValueError:
                print('Invalid input.')

        # Should not get here
        return -1


class ConnectFourRandomPlayer(ConnectFourPlayer):
    def __init__(self, model):
        self.model = model

    def get_move(self):
        moves = self.model.get_valid_moves()
        m = random.randrange(7)
        while not moves[m]:
            m = random.randrange(7)
        return m


class ConnectFourAIPlayer(ConnectFourPlayer):
        def __init__(self, model, player_num):
            self.model = model
            self.player_num = player_num
            self.max_depth = 6

        def dumb_get_move(self):
            """
            Dumb get move returns the first open spot from left to right
            """
            valid_moves = self.model.get_valid_moves()

            for i in range(7):
                if valid_moves[i]:
                    return i

        def get_move(self):
            """
            Get move for AI player
            """
            state = self.model.get_grid()

            v, a = self.max_value(state, -(math.inf), math.inf, 0)

            return a

        def max_value(self, state, alpha, beta, current_depth):

            if self.terminal_test(state):           #Checks for terminal state
                return self.utility(state), None

            if current_depth == self.max_depth:     #Evaluates the state
                return self.eval(state), None

            valid_moves = self.actions(state)
            v = -(math.inf)

            next_action = None

            for action in valid_moves:
                #Calls min value to find the next v value and incraments current_depth
                v1 = self.min_value(self.result(state, action), alpha, beta, current_depth+1)[0]

                #Checks which v value is greater
                if v1 > v:
                    v = v1
                    next_action = action

                if v >= beta:
                    return v, action

                alpha = max(alpha, v)

            return v, next_action

        def min_value(self, state, alpha, beta, current_depth):

            if self.terminal_test(state):           #Checks for terminal state
                return self.utility(state), None

            if current_depth == self.max_depth:     #Evaluates the state
                return self.eval(state), None

            valid_moves = self.actions(state)
            v = math.inf

            next_action = None

            for action in valid_moves:
                #Calls max value to find the next v value and incraments current_depth
                v1 = self.max_value(self.result(state, action), alpha, beta, current_depth+1)[0]

                #Checks which v value is greater
                if v1 < v:
                    v = v1
                    next_action = action

                if v <= alpha:
                    return v, action

                beta = min(beta, v)

            return v, next_action

        def find_other_player(self):
            """
            Finds what number value the other player
            """
            if self.player_num == 1:
                other_player = 2
            elif self.player_num == 2:
                other_player = 1

            return other_player

        def utility(self, state):
            """
            Determines who is in a win state and returns corresponding value
            """
            other_player = self.find_other_player()

            if self.check_for_winner(state) == self.player_num:
                return 1000
            elif self.check_for_winner(state) == other_player:
                return -1000
            elif self.check_for_draw(state):
                return 0

            return 0

        def eval(self, state):
            """
            Evalues current state, based on how many 3 in a rows, 2 in a rows,
            and single pieces each player has
            """
            other_player = self.find_other_player()

            ai_streaks = []
            other_streaks = []
            ai_total = 0
            other_total = 0

            #Horizontal test
            for row in range(6):
                for col in range(4):
                    #AI player
                    if state[col][row] == self.player_num:
                        if (state[col][row] == state[col + 1][row]) and (
                            state[col][row] == state[col + 2][row]):
                            ai_streaks.append(3)

                        elif (state[col][row] == state[col + 1][row]):
                            ai_streaks.append(2)

                        else:
                            ai_streaks.append(1)
                    #Other player
                    elif state[col][row] == other_player:
                        if (state[col][row] == state[col + 1][row]) and (
                            state[col][row] == state[col + 2][row]):
                            other_streaks.append(3)

                        elif (state[col][row] == state[col + 1][row]):
                            other_streaks.append(2)

                        else:
                            other_streaks.append(1)

            #Verticle test
            for col in range(7):
                for row in range(3):
                    #AI player
                    if state[col][row] == self.player_num:
                        if (state[col][row] == state[col][row + 1]) and (
                            state[col][row] == state[col][row + 2]):
                            ai_streaks.append(3)

                        elif (state[col][row] == state[col][row + 1]):
                            ai_streaks.append(2)

                        else:
                            ai_streaks.append(1)

                    #Other player
                    elif state[col][row] == other_player:
                        if (state[col][row] == state[col][row + 1]) and (
                            state[col][row] == state[col][row + 2]):
                            other_streaks.append(3)

                        elif (state[col][row] == state[col][row + 1]):
                            other_streaks.append(2)

                        else:
                            other_streaks.append(1)

            #Negative Diagonal
            for col in range(4):
                for row in range(3):
                    #AI player
                    if state[col][row] == self.player_num:
                        if (state[col][row] == state[col + 1][row + 1]) and (
                            state[col][row] == state[col + 2][row + 2]):
                            ai_streaks.append(3)

                        elif (state[col][row] == state[col + 1][row + 1]):
                            ai_streaks.append(2)

                        else:
                            ai_streaks.append(1)

                    #Other player
                    elif state[col][row] == other_player:
                        if (state[col][row] == state[col + 1][row + 1]) and (
                            state[col][row] == state[col + 2][row + 2]):
                            other_streaks.append(3)

                        elif (state[col][row] == state[col + 1][row + 1]):
                            other_streaks.append(2)

                        else:
                            other_streaks.append(1)

            #Positive Diagonal
            for col in range(3, 7):
                for row in range(3):
                    #AI player
                    if state[col][row] == self.player_num:
                        if (state[col][row] == state[col - 1][row + 1]) and (
                            state[col][row] == state[col - 2][row + 2]):
                            ai_streaks.append(3)

                        elif (state[col][row] == state[col - 1][row + 1]):
                            ai_streaks.append(2)

                        else:
                            ai_streaks.append(1)

                    #Other player
                    elif state[col][row] == other_player:
                        if (state[col][row] == state[col - 1][row + 1]) and (
                            state[col][row] == state[col - 2][row + 2]):
                            other_streaks.append(3)

                        elif (state[col][row] == state[col - 1][row + 1]):
                            other_streaks.append(2)

                        else:
                            other_streaks.append(1)

            #Totals the value for the ai players streals
            for i in ai_streaks:
                if i == 3:
                    ai_total += (3 * 100)       #3 in a row rated 100
                elif i == 2:
                    ai_total += (2 * 10)        #2 in a row rated 10
                elif i == 1:
                    ai_total += 1               #1 rated 10

            for i in other_streaks:
                if i == 3:
                    other_total += (3 * 100)
                elif i == 2:
                    other_total += (2 * 10)
                elif i == 1:
                    other_total += 1

            return (ai_total - other_total)

        def terminal_test(self, state):
            """
            Returns true if their is a terminal state
            """
            if (self.check_for_winner(state) > 0):
                return True
            if (self.check_for_draw(state)):
                return True
            else:
                return False

        """
        Checks for win and draw, based on code from model
        """
        def check_for_winner(self, state):
            win = self.__check_horizontal_win(state)
            if win < 0:
                win = self.__check_vertical_win(state)
            if win < 0:
                win = self.__check_neg_diagonal_win(state)
            if win < 0:
                win = self.__check_pos_diagonal_win(state)

            return win

        def __check_horizontal_win(self, state):
            win = False
            for row in range(6):
                for col in range(4):
                    if state[col][row] != -1:
                        win = (state[col][row] == state[col + 1][row]) and (
                            state[col][row] == state[col + 2][row]) and (
                                  state[col][row] == state[col + 3][row])
                    if win:
                        return state[col][row]
            return -1

        def __check_vertical_win(self, state):
            win = False
            for col in range(7):
                for row in range(3):
                    if state[col][row] != -1:
                        win = (state[col][row] == state[col][row + 1]) and (
                            state[col][row] == state[col][row + 2]) and (
                                  state[col][row] == state[col][row + 3])
                    if win:
                        return state[col][row]
            return -1

        def __check_neg_diagonal_win(self, state):
            win = False
            for col in range(4):
                for row in range(3):
                    if state[col][row] != -1:
                        win = (state[col][row] == state[col + 1][row + 1]) and (
                            state[col][row] == state[col + 2][row + 2]) and (
                                  state[col][row] == state[col + 3][row + 3])
                    if win:
                        return state[col][row]
            return -1

        def __check_pos_diagonal_win(self, state):
            win = False
            for col in range(3, 7):
                for row in range(3):
                    if state[col][row] != -1:
                        win = (state[col][row] == state[col - 1][row + 1]) and (
                            state[col][row] == state[col - 2][row + 2]) and (
                                  state[col][row] == state[col - 3][row + 3])
                    if win:
                        return state[col][row]
            return -1

        def check_for_draw(self, state):
            for i in range(7):
                for j in range(6):
                    if state[i][j] == -1:
                        return False
            return True

        def actions(self, state):
            """
            Returns all valid moves for the state
            """
            action_list = []

            for i in range(7):
                if(state[i][0] == -1):
                    action_list.append(i)

            return action_list

        def result(self, state, action):
            """
            Returns the state after the action is taken
            """
            state_copy = copy.deepcopy(state)

            player = self.find_player(state_copy)       #Finds the next player

            #Finds row to place piece in
            row = 0
            for i in range(0, 6):

                if state_copy[action][i] == -1:
                    row = i

            state_copy[action][row] = player

            return state_copy

        def find_player(self, grid):
            """
            Finds the next player based on the number of pieces placed
            """
            count1 = 0
            count2 = 0

            for i in range(7):
                for j in range(6):

                    if grid[i][j] == 1:
                        count1 += 1

                    elif grid[i][j] == 2:
                        count2 += 1

            if count1 > count2:
                return 2

            elif count1 == count2:
                return 1
