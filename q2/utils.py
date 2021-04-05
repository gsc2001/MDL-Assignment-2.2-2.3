from enum import Enum, IntEnum


class Action(str, Enum):
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
    W = 0
    N = 1
    E = 2
    S = 3
    C = 4


class MMState(IntEnum):
    Dormant = 0
    Ready = 1


class MMHealth(IntEnum):
    _0 = 0
    _25 = 1
    _50 = 2
    _75 = 3
    _100 = 4


# class State:
#     def __init__(self, pos: Position, mat, arrow, mm_state: MMState, mm_health):
#         self.pos = pos
#         self.mat = mat
#         self.arrow = arrow
#         self.mm_state = mm_state
#         self.mm_health = mm_health
#
#     def __str__(self):
#         return f'<{self.pos}, {self.mat}, {self.arrow}, {self.mm_state}, {self.mm_health}>'
