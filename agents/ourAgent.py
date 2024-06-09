import random
import numpy as np
from gym_env.enums import Action

size = (
    100, #equity
    
)


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, env = "", weights=[], name='Learner'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.env = env
        self.weights = weights

    def roundOver(self, reward):
        print("round over\n\n")
        pass

    def action(self, action_space, observation, info):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        _ = info
        if not self.weights:
            self.weights = np.ndarray((1,1))
        

        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HALF_POT,
                                    Action.RAISE_2POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action
