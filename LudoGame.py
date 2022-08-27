# Author: Ray Zhao
# GitHub username: rzhao315
# Date: 8/11/2022
# Description: Ludo Game Portfolio Project


class Player:
    """The Player object represents the player who plays the game at a certain position. """

    def __init__(self, position):
        self._position = position
        if self._position == 'A':
            self._start_space = 1
            self._end_space = 57
        if self._position == 'B':
            self._start_space = 15
            self._end_space = 8
        if self._position == 'C':
            self._start_space = 29
            self._end_space = 22
        if self._position == 'D':
            self._start_space = 43
            self._end_space = 36

        self._p_position = 'H'  # ‘H’ for home yard, ‘R’ for ready to go position, ‘E’ for finished position for p token
        self._q_position = 'H'  # ‘H’ for home yard, ‘R’ for ready to go position, ‘E’ for finished position for q token
        self._token_p_step_count = -1  #-1 is home and 0 is ready to go - p token
        self._token_q_step_count = -1  #-1 is home and 0 is ready to go - q token
        self._is_stacked = False
        self._current_state = "Still playing"  # the current state of the player: whether the player has won and finished the game, or is still playing
        self._complete_game = False

    def get_completed(self):
        """takes no parameters and returns True or False if the player has finished or not finished the game"""
        return self._complete_game

    def set_complete(self, game_complete):
        """setter for completing game, set to True if game is complete"""
        self._complete_game = game_complete

    def get_current_state(self):
        """get method for current state of the game"""
        return self._current_state

    def set_current_state(self, status):
        """set method for completing game, if both tokens are 'E' and reached 57 steps, return 'Finished"""
        self._current_state = status

    def get_token_p_step_count(self):
        """ takes no parameters and returns the total steps the token p has taken on the board (use steps = -1 for home yard position and steps = 0 for ready to go position)"""
        return self._token_p_step_count

    def get_token_q_step_count(self):
        """ takes no parameters and returns the total steps the token q has taken on the board (use steps = -1 for home yard position and steps = 0 for ready to go position)"""
        return self._token_q_step_count

    def set_token_p_step_count(self, num):
        """set method for p token"""
        self._token_p_step_count = num

    def set_token_q_step_count(self, num):
        """set method for q token"""
        self._token_q_step_count = num

    def get_space_name(self, total_steps):
        """parameter the total steps of the token and returns the name of the space the token has landed on on the board as a string. It should be able to return the home yard position (‘H’) and the ready to go position (‘R’) as well. ('E') represents finish position.
        """
        if total_steps == 0:
            return "R"  # ready to go position
        if total_steps == -1:
            return "H"  # home yard position
        if total_steps == 57:
            return "E"  # finished game position
        if total_steps == 1:  # starting position for each player
            return str(self._start_space)
        if 50 < total_steps < 57:
            return self._position + str(total_steps - 50)  # returns the player's home squares
        if self._position == 'A':
            new_steps = total_steps
            return str(new_steps)
        if self._position == 'B' or 'C' or 'D':
            new_steps = (self._start_space + total_steps - 1)  # mod is max 56 steps, returns space step for player [B,C,D]
            if new_steps > 57:
                return str(new_steps % 56)
            return str(new_steps)

    def get_position(self):
        """get method that represents players"""
        return self._position

    def get_start_space(self):
        """get method to start the space for specific player"""
        return self._start_space

    def get_end_space(self):
        """get method to end the space for specific player"""
        return self._end_space

    def is_stacked(self):
        """get method for stacked tokens"""
        return self._is_stacked

    def set_stacked(self, T_or_F):
        """set method for stacking two tokens, True for stacked and false for not stacked"""
        self._is_stacked = T_or_F

    def get_p_position(self):
        """get method for p token"""
        return self._p_position

    def get_q_position(self):
        """get method for q token"""
        return self._q_position

    def set_p_position(self, string):
        """set method for p token, 'H','R', or "e"'"""
        self._p_position = string

    def set_q_position(self, string):
        """set method for q token, 'H','R', or "e"'"""
        self._q_position = string


class LudoGame:
    """LudoGame object represents the game as played."""

    def __init__(self):
        self._player_list = []
        self._turn_list = []

    def get_player_by_position(self, player_pos):
        """ takes a parameter representing the player’s position as a string and returns the player object. For an invalid string parameter, it will return "Player not found!"""
        for player in self._player_list:
            if player_pos == player.get_position():
                return player

        return "Player not found!"

    def play_game(self, players, turns_list):
        """The players list is the list of positions players choose, like [‘A’, ‘C’] means two players will play the game at position A and C. Turns list is a list of tuples with each tuple a roll for one player."""

        move_list = []
        for player in players:
            self._player_list.append(Player(player))

        for turns in turns_list:
            for position_obj in self._player_list:
                position = turns[0]
                move_steps = turns[1]
                if position_obj.get_position() == position:
                    player_obj = self.get_player_by_position(position)
                    token_name = self.priority_rules(move_steps, position_obj, self._player_list)
                    self.move_token(player_obj, token_name, move_steps)
        for position_obj in self._player_list:
            move_list.append(position_obj.get_space_name(position_obj.get_token_p_step_count()))
            move_list.append(position_obj.get_space_name(position_obj.get_token_q_step_count()))
        return move_list

    def move_token(self, player_obj, token_name, move_steps):
        """method takes three parameters, the player object, the token name (‘p’ or ‘q’) and the steps the token will move on the board (int). This method will take care of one token moving on the board."""

        if token_name == "p_R":
            player_obj.set_p_position("R")
            player_obj.set_token_p_step_count(0)
        if token_name == "q_R":
            player_obj.set_q_position("R")
            player_obj.set_token_q_step_count(0)

        if token_name == "p_E":
            player_obj.set_p_position("E")
            player_obj.set_token_p_step_count(57)
        if token_name == "q_E":
            player_obj.set_q_position("E")
            player_obj.set_token_q_step_count(57)

        if token_name == "q_E" and "p_E":
            player_obj.set_p_position("E")
            player_obj.set_q_position("E")
            player_obj.set_complete(True)
            player_obj.set_current_state("Finished")


        # priority 3
        if token_name == 'opponent_p_H':
            player_obj.set_token_p_step_count(player_obj.get_token_p_step_count() + int(move_steps))

        if token_name == 'opponent_q_H':
            player_obj.set_token_q_step_count(player_obj.get_token_q_step_count() + int(move_steps))

        # priority 4
        elif token_name == 'move_p':
            if player_obj.get_token_p_step_count() + int(move_steps) > 57: #bounce back token if turns are over 57 for p token
                bounce_step = player_obj.get_token_p_step_count() + int(move_steps) - 57
                return player_obj.set_token_p_step_count(57 - bounce_step)
            player_obj.set_token_p_step_count(player_obj.get_token_p_step_count() + int(move_steps))
        elif token_name == 'move_q':
            if player_obj.get_token_q_step_count() + int(move_steps) > 57:  #bounce back token if turns are over 57 for q token
                bounce_step = player_obj.get_token_q_step_count() + int(move_steps) - 57
                return player_obj.set_token_q_step_count(57 - bounce_step)
            player_obj.set_token_q_step_count(player_obj.get_token_q_step_count() + int(move_steps))

        elif player_obj.get_token_p_step_count() == player_obj.get_token_p_step_count():
            if player_obj.get_token_p_step_count() != -0 and player_obj.get_token_q_step_count() != 0:
                if player_obj.get_token_p_step_count() != -1 and player_obj.get_token_q_step_count() != -1:
                    player_obj.set_stacked(True)

        elif player_obj.is_stacked():
            if player_obj.get_token_p_step_count() < player_obj.get_token_q_step_count():
                player_obj.set_token_p_step_count(player_obj.get_token_q_step_count())
            if player_obj.get_token_q_step_count() < player_obj.get_token_p_step_count():
                player_obj.set_token_q_step_count(player_obj.get_token_p_step_count())

        if token_name == 'move_p_q':  #move both stacked tokens
            player_obj.set_token_p_step_count(player_obj.get_token_p_step_count() + int(move_steps))
            player_obj.set_token_q_step_count(player_obj.get_token_q_step_count() + int(move_steps))

    def priority_rules(self, move_steps, player_obj, all_players_list):
        """ 1. Rolled a 6:
                Moving from your ‘H’ to ‘R’ is first priority (if you still have tokens in your Home Yard).
               If both tokens are in ‘H’, token ‘p’ is moved out first.
            2. If token is in the home square and die roll is exactly what is needed to reach the final space, move token
                to final space.
            3. If token can move and land on opponent’s token(s), then land on opponent’s token.
            4. Furthest token away from final space moves
        """
        # priority 1
        if move_steps == 6:
            if player_obj.get_p_position() == 'H':
                return 'p_R'
            elif player_obj.get_q_position() == 'H':
                return 'q_R'
        # priority 2 - If token is in the home square and die roll is exactly what is needed to reach the final space, move token to final space.
        if player_obj.get_token_p_step_count() + move_steps == 57:
            return 'p_E'
        if player_obj.get_token_q_step_count() + move_steps == 57:
            return 'q_E'
        if player_obj.get_p_position() == 'E':  #if p token reached end space, set p to 'E'
            return 'p_E'
        if player_obj.get_q_position() == 'E':  #if q token reached end space, set p to 'E'
            return 'q_E'


        # priority 3 - If token can move and land on opponent’s token(s), then land on opponent’s token.
        for opponent in all_players_list:
            if player_obj.get_position() != opponent.get_position():

                if player_obj.get_space_name(player_obj.get_token_p_step_count() + move_steps) == opponent.get_space_name(opponent.get_token_p_step_count()):
                    opponent.set_p_position('H')
                    opponent.set_token_p_step_count(-1)
                    return 'opponent_p_H'
                if player_obj.get_space_name(player_obj.get_token_p_step_count() + move_steps) == opponent.get_space_name(opponent.get_token_q_step_count()):
                    opponent.set_q_position('H')
                    opponent.set_token_q_step_count(-1)
                    return 'opponent_q_H'
                if player_obj.get_space_name(player_obj.get_token_q_step_count() + move_steps) == opponent.get_space_name(opponent.get_token_p_step_count()):
                    opponent.set_p_position('H')
                    opponent.set_token_p_step_count(-1)
                    return 'opponent_p_H'
                if player_obj.get_space_name(player_obj.get_token_q_step_count() + move_steps) == opponent.get_space_name(opponent.get_token_q_step_count()):
                    opponent.set_q_position('H')
                    opponent.set_token_q_step_count(-1)
                    return 'opponent_q_H'
            else:
                if player_obj.get_space_name(player_obj.get.token_q_step()) + move_steps == player_obj.get_space_name(player_obj.get.token_p_step()) + move_steps:



        # priority 4 - Furthest token away from final space moves
        if player_obj.get_token_p_step_count() >= 0 and player_obj.get_token_q_step_count() == -1:
            return 'move_p'
        if player_obj.get_token_q_step_count() >= 0 and player_obj.get_token_p_step_count() == -1:
            return 'move_q'
        if player_obj.get_token_p_step_count() < player_obj.get_token_q_step_count():
            return 'move_p'
        if player_obj.get_token_q_step_count() < player_obj.get_token_p_step_count():
            return 'move_q'
        # stacked moving as one
        if player_obj.get_token_p_step_count() == player_obj.get_token_q_step_count():
            return 'move_p_q'


players = ['A','B']
turns = [('A', 6),('A', 2),('A', 2),('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('B', 6),('B', 3)]
['3', 'H', '17', 'H']
# players = ['A', 'B']
# turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4), ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
game = LudoGame()
current_tokens_space = game.play_game(players, turns)
print(current_tokens_space)
player_A = game.get_player_by_position('A')
# # print(player_A.get_completed())
# # print(player_A.get_token_p_step_count())
# #
player_B = game.get_player_by_position('B')
# print(player_A.get_space_name(55))
