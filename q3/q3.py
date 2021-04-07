from typing import List, Dict

import cvxpy as cp
import numpy as np

from utils import *
from constants import *

# x [ (), (), (), .... ]

r = []


# n_actions = 1936

# states = []
# states.append(state)

# A
# 600 x 1936
#


# [pos, mat, arrow, mm_state, mm_health]


def main():
    u_d = np.ndarray((5, 3, 4, 2, 5), dtype=float)
    u = np.ndarray(u_d.shape, dtype=float)
    actions = np.ndarray(u_d.shape, dtype=object)
    u_d[:] = 0
    iteration = 0
    a = np.ndarray((600, 1936))

    def log(_state: State, action_type, action_utility):
        # print(f"{_state} : {action_type} = [ {action_utility} ]")
        actions[_state.index()] = action_type

    n_actions = 0

    u[:] = u_d[:]
    print(f"iteration={iteration}")
    iteration += 1

    action_index = 0

    for pos in Position:
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:
                        if mm_health == MMHealth.h0:
                            state = None
                            if pos == Position.C:
                                state = State(Position.C, mat, arrow, mm_state, mm_health, action_index)
                            elif pos == Position.N:
                                state = State(Position.N, mat, arrow, mm_state, mm_health, action_index)
                            elif pos == Position.S:
                                state = State(Position.S, mat, arrow, mm_state, mm_health, action_index)
                            elif pos == Position.E:
                                state = State(Position.E, mat, arrow, mm_state, mm_health, action_index)
                            elif pos == Position.W:
                                state = State(Position.W, mat, arrow, mm_state, mm_health, action_index)
                            state.possible_actions.append(Action(ActionType.NONE, []))
                            action_index += len(state.possible_actions)
                            state.populate_a(a)
                            continue

                        if pos == Position.C:
                            state = State(Position.C, mat, arrow, mm_state, mm_health, action_index)

                            # movement
                            state.possible_actions.extend([
                                Action(action_type=ActionType.UP, states=[
                                    (0.85, State(**state.update(pos=Position.N))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.DOWN, states=[
                                    (0.85, State(**state.update(pos=Position.S))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.LEFT, states=[
                                    (0.85, State(**state.update(pos=Position.W))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.RIGHT, states=[
                                    (0.85, State(**state.update(pos=Position.E))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.STAY, states=[
                                    (0.85, State(**state.update(pos=Position.C))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                            ])

                            # shoot
                            if arrow > 0:
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.SHOOT, states=[
                                        (0.5, State(
                                            **state.update(arrow=state.arrow - 1))),
                                        (0.5, State(
                                            **state.update(arrow=state.arrow - 1, mm_health=state.mm_health - 1))),
                                    ]),
                                ])

                            state.possible_actions.extend([
                                Action(action_type=ActionType.HIT, states=[
                                    (0.1, State(
                                        **state.update(mm_health=max(state.mm_health - 2, 0)))),
                                    (0.9, State(**state.update())),
                                ]),
                            ])

                            state.populate_a(a)
                            action_index += len(state.possible_actions)


                        elif pos == Position.N:

                            state = State(Position.N, mat, arrow, mm_state, mm_health, action_index)

                            # movement
                            state.possible_actions.extend([
                                Action(action_type=ActionType.DOWN, states=[
                                    (0.85, State(**state.update(pos=Position.C))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.STAY, states=[
                                    (0.85, State(**state.update(pos=Position.N))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                            ])

                            # craft
                            if mat > 0:
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.CRAFT, states=[
                                        (0.5, State(
                                            **state.update(mat=state.mat - 1, arrow=min(state.arrow + 1, 3)))),
                                        (0.35, State(
                                            **state.update(mat=state.mat - 1, arrow=min(state.arrow + 2, 3)))),
                                        (0.15, State(
                                            **state.update(mat=state.mat - 1, arrow=min(state.arrow + 3, 3)))),
                                    ])
                                ])

                            state.populate_a(a)
                            action_index += len(state.possible_actions)


                        elif pos == Position.S:
                            state = State(Position.S, mat, arrow, mm_state, mm_health, action_index)

                            # movement
                            state.possible_actions.extend([
                                Action(action_type=ActionType.UP, states=[
                                    (0.85, State(**state.update(pos=Position.C))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                                Action(action_type=ActionType.STAY, states=[
                                    (0.85, State(**state.update(pos=Position.S))),
                                    (0.15, State(**state.update(pos=Position.E))),
                                ]),
                            ])

                            # gather
                            state.possible_actions.extend([
                                Action(action_type=ActionType.CRAFT, states=[
                                    (0.75, State(
                                        **state.update(mat=min(state.mat + 1, 2)))),
                                    (0.25, State(
                                        **state.update(mat=min(state.mat + 0, 2)))),
                                ])
                            ])

                            n_actions += 3

                            state.populate_a(a)
                            action_index += len(state.possible_actions)

                        elif pos == Position.E:
                            state = State(Position.E, mat, arrow, mm_state, mm_health, action_index)

                            # movement
                            state.possible_actions.extend([
                                Action(action_type=ActionType.LEFT, states=[
                                    (1, State(
                                        **state.update(pos=(Position.W if T2C1 else Position.C)))),
                                ]),
                                Action(action_type=ActionType.STAY, states=[
                                    (1, State(**state.update(pos=Position.E))),
                                ]),
                            ])
                            n_actions += 2

                            # shoot
                            if arrow > 0:
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.SHOOT, states=[
                                        (0.1, State(
                                            **state.update(arrow=state.arrow - 1))),
                                        (0.9, State(
                                            **state.update(arrow=state.arrow - 1, mm_health=state.mm_health - 1))),
                                    ]),
                                ])
                                n_actions += 1

                            # hit
                            state.possible_actions.extend([
                                Action(action_type=ActionType.HIT, states=[
                                    (0.2, State(
                                        **state.update(mm_health=max(state.mm_health - 2, 0)))),
                                    (0.8, State(**state.update())),
                                ]),
                            ])
                            n_actions += 1

                            state.populate_a(a)
                            action_index += len(state.possible_actions)

                        elif pos == Position.W:
                            state = State(Position.W, mat, arrow, mm_state, mm_health, action_index)

                            # movement
                            state.possible_actions.extend([
                                Action(action_type=ActionType.RIGHT, states=[
                                    (1, State(**state.update(pos=Position.C))),
                                ]),
                                Action(action_type=ActionType.STAY, states=[
                                    (1, State(**state.update(pos=Position.W))),
                                ]),
                            ])
                            n_actions += 2

                            # shoot
                            if arrow > 0:
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.SHOOT, states=[
                                        (0.75, State(
                                            **state.update(arrow=state.arrow - 1))),
                                        (0.25, State(
                                            **state.update(arrow=state.arrow - 1, mm_health=state.mm_health - 1))),
                                    ]),
                                ])
                                n_actions += 1

                            state.populate_a(a)
                            action_index += len(state.possible_actions)

    print('\n\n\n\n\n')
    print(n_actions)


if __name__ == '__main__':
    main()