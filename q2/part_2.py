from typing import List, Dict

import numpy as np

from utils import *
from constants import *


# [pos, mat, arrow, mm_state, mm_health]


def main():
    u_d = np.ndarray((5, 3, 4, 2, 5), dtype=float)
    u = np.ndarray(u_d.shape, dtype=float)
    actions = np.ndarray(u_d.shape, dtype=object)
    u_d[:] = 0
    iteration = 0

    def log(_state: State, action_type, action_utility):
        print(f"{_state} : {action_type} = [ {np.round(action_utility, decimals=3)} ]")
        actions[_state.index()] = action_type

    while True:
        u[:] = u_d[:]
        print(f"iteration={iteration}")
        iteration += 1

        for pos in Position:
            for mat in [0, 1, 2]:
                for arrow in [0, 1, 2, 3]:
                    for mm_state in MMState:
                        for mm_health in MMHealth:
                            if mm_health == MMHealth.h0:
                                if pos == Position.C:
                                    state = State(Position.C, mat, arrow,
                                                  mm_state, mm_health)
                                    log(state, ActionType.NONE, 0)
                                elif pos == Position.N:
                                    state = State(Position.N, mat, arrow,
                                                  mm_state, mm_health)
                                    log(state, ActionType.NONE, 0)
                                elif pos == Position.S:
                                    state = State(Position.S, mat, arrow,
                                                  mm_state, mm_health)
                                    log(state, ActionType.NONE, 0)
                                elif pos == Position.E:
                                    state = State(Position.E, mat, arrow,
                                                  mm_state, mm_health)
                                    log(state, ActionType.NONE, 0)
                                elif pos == Position.W:
                                    state = State(Position.W, mat, arrow,
                                                  mm_state, mm_health)
                                    log(state, ActionType.NONE, 0)
                                continue

                            if pos == Position.C:
                                state = State(Position.C, mat, arrow,
                                              mm_state, mm_health)

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

                                best_action = state.get_best_action(u)
                                u_d[state.index()] = best_action.utility
                                log(state, best_action.action_type,
                                    best_action.utility)

                            elif pos == Position.N:
                                state = State(Position.N, mat, arrow,
                                              mm_state, mm_health)

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

                                best_action = state.get_best_action(u)
                                u_d[state.index()] = best_action.utility
                                log(state, best_action.action_type,
                                    best_action.utility)

                            elif pos == Position.S:
                                state = State(Position.S, mat, arrow,
                                              mm_state, mm_health)

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
                                    Action(action_type=ActionType.GATHER, states=[
                                        (0.75, State(
                                            **state.update(mat=min(state.mat + 1, 2)))),
                                        (0.25, State(
                                            **state.update(mat=min(state.mat + 0, 2)))),
                                    ])
                                ])

                                best_action = state.get_best_action(u)
                                u_d[state.index()] = best_action.utility
                                log(state, best_action.action_type,
                                    best_action.utility)

                            elif pos == Position.E:
                                state = State(Position.E, mat, arrow,
                                              mm_state, mm_health)

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

                                # hit
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.HIT, states=[
                                        (0.2, State(
                                            **state.update(mm_health=max(state.mm_health - 2, 0)))),
                                        (0.8, State(**state.update())),
                                    ]),
                                ])

                                best_action = state.get_best_action(u)
                                u_d[state.index()] = best_action.utility
                                log(state, best_action.action_type,
                                    best_action.utility)

                            elif pos == Position.W:
                                state = State(Position.W, mat, arrow,
                                              mm_state, mm_health)

                                # movement
                                state.possible_actions.extend([
                                    Action(action_type=ActionType.RIGHT, states=[
                                        (1, State(**state.update(pos=Position.C))),
                                    ]),
                                    Action(action_type=ActionType.STAY, states=[
                                        (1, State(**state.update(pos=Position.W))),
                                    ]),
                                ])

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

                                best_action = state.get_best_action(u)
                                u_d[state.index()] = best_action.utility
                                log(state, best_action.action_type,
                                    best_action.utility)

        if np.max(np.abs(u_d[:] - u[:])) < delta:
            break


if __name__ == '__main__':
    main()
