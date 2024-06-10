import random
import numpy as np
import time
from gym_env.enums import Action

size = (
    100, #equity
)


class Player:
    """Mandatory class with the player methods"""

    def __init__(self, env = "", qtable=[], alphas=[], fromFile=False, writeFile=False, name='Learner'):
        """Initiaization of an agent"""
        self.equity_alive = 0
        self.actions = []
        self.last_action_in_stage = ''
        self.temp_stack = []
        self.name = name
        self.env = env
        self.curActions = []
        self.shape = shape = (100,10,10, 4, env.action_space.n)
        if fromFile:
            self.qtable = np.fromfile("qWeights").reshape(shape)
            self.alphas = np.fromfile("alphas").reshape(shape)
        else:
            self.qtable = np.ndarray(self.shape)
            self.alphas = np.ndarray(self.shape)
        
    def trainDone(self):
        self.qtable.tofile("qWeights")
        self.alphas.tofile("alphas")
        
    def gameDone(self, round):
        pass
    
    def adjust_weights(self, weights):
        min_weight = np.min(weights)
        if min_weight < 0:
            # Shift weights by adding the absolute value of the smallest weight
            weights = weights + abs(min_weight)
        # Normalize weights to sum to 1
        total_weight = np.sum(weights)
        if total_weight > 0:
            weights = weights / total_weight
        else:
            return [1/len(weights),] * len(weights)
        return weights    
    
    
    def getAction(self, epsilon=.2):
        env = self.env
        alpha_table = self.alphas
        q_table = self.qtable
        moves, obs, info = env.legal_moves, env.observation, env.info
        
        ourStack = int(info['stage_data'][0]["stack_at_action"][1]*10)//5
        hisStack = int(info['stage_data'][0]["stack_at_action"][0]*10)//5
        equity = int(info['player_data']['equity_to_river_alive']*100)
        ourstack = min(9,ourStack)
        hisStack = min(9, hisStack)
        equity = min(99,equity)
        round = env.stage.value

        tableArgs = (equity, ourStack, hisStack, int(round))
        
        possibleActions = self.qtable[tableArgs]
        moves = [x.value for x in moves]
        allowedActions = [n for n in range(8) if n in moves ]
        if random.random()<epsilon:
            curaction = random.choice(range(len(allowedActions)))
        else:
            curaction = np.random.choice(len(q_table[tableArgs][allowedActions]), p=self.adjust_weights(q_table[tableArgs][allowedActions]))
        curaction = allowedActions[curaction]
        access =  tableArgs + (curaction,)
        alpha = alpha_table[access] +1
        alpha_table[access] = alpha
        self.curActions.append(access)
        return curaction
        
    

    def roundOver(self, reward):
        print("round over\n\n")
        q_table = self.qtable
        for n,access in enumerate(self.curActions):
            alpha = self.alphas[access]
            gamma = .7**(len(self.curActions)-n)
            weightedReward = (1/alpha)*(gamma)*(reward - q_table[access])/10
            print(access, alpha, weightedReward)
            q_table[access] = weightedReward
        self.curActions = []

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
