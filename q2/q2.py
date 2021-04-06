from typing import List, Dict

import numpy as np

from utils import *
from constants import *


# [pos, mat, arrow, mm_state, mm_health]


def main():
    u_d = np.ndarray((5, 3, 4, 2, 5), dtype=float)
    u = np.ndarray(u_d.shape, dtype=float)
    u_d[:] = 0
    iteration = 0

    while True:
        u[:] = u_d[:]
        print(f"iteration={iteration}")
        iteration += 1

        for mm_state in MMState:
            for mat in [0, 1, 2]:
                for arrow in [0, 1, 2, 3]:
                    for mm_health in MMHealth:
                        if mm_health == MMHealth.h0:
                            continue

                        # Position : C
                        state = State(Position.C, mat, arrow, mm_state, mm_health)

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
                                    (0.5, State(**state.update(arrow=state.arrow - 1))),
                                    (0.5, State(**state.update(arrow=state.arrow - 1, mm_health=state.mm_health - 1))),
                                ]),
                            ])

                        state.possible_actions.extend([
                            Action(action_type=ActionType.HIT, states=[
                                (0.1, State(**state.update(mm_health=max(state.mm_health - 2)))),
                                (0.9, State(**state.update())),
                            ]),
                        ])

                        best_action = state.get_best_action(u)
                        u_d[state.index()] = best_action.utility
                        print(f"{state}:{best_action.action_type} = [{best_action.utility}]")

                        # north square

                        # possible_actions = {}
                        #
                        # def movementN(new_pos: Position):
                        #     return 0.85 * u[new_pos, mat, arrow, mm_state, mm_health] + 0.15 * u[
                        #         Position.E, mat, arrow, mm_state, mm_health]
                        #
                        # def craft(arrows: int):
                        #     return u[Position.N, mat - 1, min(3, arrow + arrows), mm_state, mm_health]
                        #
                        # # movement
                        # possible_actions.update({
                        #     ActionType.DOWN: movementN(Position.C),
                        #     ActionType.STAY: movementN(Position.N)
                        # })
                        #
                        # # craft
                        # if mat > 0:
                        #     possible_actions.update({
                        #         ActionType.CRAFT: 0.5 * craft(1) + 0.35 * craft(2) + 0.15 * craft(3)
                        #     })
                        #
                        # values = np.array(list(possible_actions.values()))
                        # actions = np.array(list(possible_actions.keys()))
                        # values = step_cost + gamma * values
                        # idx = values.argmax()
                        # u_d[Position.N, mat, arrow, mm_state, mm_health] = values[idx]
                        #
                        # print(
                        #     f"({Position.N}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                        #     {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

                        # south square
                        possible_actions = {}

                        def movementS(new_pos: Position):
                            return 0.85 * u[new_pos, mat, arrow, mm_state, mm_health] + 0.15 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        def gather(amount: int):
                            return u[Position.S, min(mat + amount, 2), arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            ActionType.UP: movementS(Position.C),
                            ActionType.STAY: movementS(Position.S)
                        })

                        # gather
                        possible_actions.update({
                            ActionType.GATHER: 0.75 * gather(1) + 0.25 * gather(0)
                        })

                        values = np.array(list(possible_actions.values()))
                        actions = np.array(list(possible_actions.keys()))
                        values = step_cost + gamma * values
                        idx = values.argmax()
                        u_d[Position.S, mat, arrow, mm_state, mm_health] = values[idx]

                        print(
                            f"({Position.S}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

                        # east square

                        possible_actions = {}

                        def movementE(new_pos: Position):
                            return u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            ActionType.LEFT: movementE(Position.C),
                            ActionType.STAY: movementE(Position.E)
                        })

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                ActionType.SHOOT: 0.1 * u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health] + 0.9 * (kill_reward + u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            })

                        # hit
                        if mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h50 or mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                ActionType.HIT: 0.8 * u[Position.C, mat, arrow, mm_state, mm_health] + 0.2 * (
                                        kill_reward + u[Position.C, mat, arrow, mm_state, max(0, mm_health - 2)])
                            })

                        values = np.array(list(possible_actions.values()))
                        actions = np.array(list(possible_actions.keys()))
                        values = step_cost + gamma * values
                        idx = values.argmax()
                        u_d[Position.E, mat, arrow, mm_state, mm_health] = values[idx]

                        print(
                            f"({Position.E}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

                        # west square

                        possible_actions = {}

                        def movementW(new_pos: Position):
                            return u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            ActionType.RIGHT: movementW(Position.C),
                            ActionType.STAY: movementW(Position.W)
                        })

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                ActionType.SHOOT: 0.75 * u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health] + 0.25 * (kill_reward + u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            })

                        values = np.array(list(possible_actions.values()))
                        actions = np.array(list(possible_actions.keys()))
                        values = step_cost + gamma * values
                        idx = values.argmax()
                        u_d[Position.W, mat, arrow, mm_state, mm_health] = values[idx]

                        print(
                            f"({Position.W}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

        if np.max(np.abs(u_d[:] - u[:])) < delta:
            break


if __name__ == '__main__':
    main()
