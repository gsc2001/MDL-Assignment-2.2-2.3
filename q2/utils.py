from typing import List, Tuple
from enum import Enum, IntEnum

import numpy as np

from constants import *


class ActionType(str, Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    STAY = 'STAY'
    SHOOT = 'SHOOT'
    HIT = 'HIT'
    CRAFT = 'CRAFT'
    GATHER = 'GATHER'
    NONE = 'NONE'


class Position(IntEnum):
    N = 0
    W = 1
    E = 2
    S = 3
    C = 4


class MMState(IntEnum):
    D = 0
    R = 1


class MMHealth(IntEnum):
    h0 = 0
    h25 = 1
    h50 = 2
    h75 = 3
    h100 = 4


class State:
    def __init__(self, pos: Position, mat, arrow, mm_state: MMState, mm_health):
        self.pos = pos
        self.mat = mat
        self.arrow = arrow
        self.mm_state = mm_state
        self.mm_health = mm_health
        self.possible_actions = []

    def __str__(self):
        return f'( {self.pos.name}, {self.mat}, {self.arrow}, {self.mm_state.name}, {self.mm_health * 25} )'

    def __iter__(self):
        for attr in [self.pos, self.mat, self.arrow, self.mm_state, self.mm_health]:
            yield attr

    def index(self) -> tuple:
        return self.pos, self.mat, self.arrow, self.mm_state, self.mm_health

    def update(self, **kwargs):
        _dict = self.__dict__.copy()
        _dict.update(kwargs)
        _dict.pop('possible_actions')
        return _dict

    def get_best_action(self, u):
        utilities = np.array([action.get_utility(u, self)
                              for action in self.possible_actions])
        idx = utilities.argmax()
        return self.possible_actions[idx]


def get_kill_reward(state: State):
    if state.mm_health == MMHealth.h0:
        return 50
    return 0


class Action:
    def __init__(self, action_type: ActionType, states: List[Tuple[float, State]]):
        self.action_type = action_type
        self.states = states
        self.utility = None

    def get_utility(self, u: np.ndarray, current_state: State):

        utility = 0
        if current_state.mm_state == MMState.D:
            for prob, state in self.states:
                utility += prob * (gamma * (0.8 * u[State(**state.update(mm_state=MMState.D)).index()] + 0.2 * u[
                    State(**state.update(mm_state=MMState.R)).index()]) + get_kill_reward(state))

        else:
            for prob, state in self.states:
                utility += 0.5 * prob * (
                        gamma * u[State(**state.update(mm_state=MMState.R)).index()] + get_kill_reward(state))

            if current_state.pos in [Position.C, Position.E]:
                utility += 0.5 * (gamma * u[State(current_state.pos, current_state.mat, 0, MMState.D,
                                                  min(4, current_state.mm_health + 1)).index()] - 40)
            else:
                for prob, state in self.states:
                    utility += 0.5 * prob * (
                            gamma * u[State(**state.update(mm_state=MMState.D)).index()] + get_kill_reward(state))

        utility += step_cost
        self.utility = utility
        return utility
