from typing import List, Dict

import numpy as np

from utils import *

# [pos, mat, arrow, mm_state, mm_health]

gamma = 0.999
delta = 0.001

team_number = 105

step_cost = -20


def main():
    u_d = np.ndarray((5, 3, 4, 2, 5), dtype=float)
    u = np.ndarray(u_d.shape, dtype=float)
    u_d[:] = 0
    iteration = 0

    while True:
        u[:] = u_d[:]
        print(f"iteration={iteration}")
        iteration += 1
        # Centre square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = {}

                        def movementC(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            Action.UP: movementC(Position.N),
                            Action.DOWN: movementC(Position.S),
                            Action.LEFT: movementC(Position.W),
                            Action.RIGHT: movementC(Position.E),
                            Action.STAY: movementC(Position.C)

                        })

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                Action.SHOOT: step_cost + 0.5 * u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health] + 0.5 * (kill_reward + u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            })

                        # hit
                        if mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h50 or mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                Action.HIT: step_cost + 0.9 * u[Position.C, mat, arrow, mm_state, mm_health] + 0.1 * (
                                        kill_reward + u[Position.C, mat, arrow, mm_state, max(0, mm_health - 2)])
                            })

                        values = np.array(possible_actions.values())
                        idx = values.argmax()
                        u_d[Position.C, mat, arrow, mm_state,
                            mm_health] = values[idx]

                        print(
                            f"({Position.C}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

        # north square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = {}

                        def movementN(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        def craft(arrows: int):
                            return u[Position.N, mat - 1, min(3, arrow + arrows), mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            Action.DOWN: movementN(Position.C),
                            Action.STAY: movementN(Position.N)
                        })

                        # craft
                        if mat > 0:
                            possible_actions.update({
                                Action.CRAFT: step_cost + 0.5 * craft(1) + 0.35 * craft(2) + 0.15 * craft(3)
                            })

                        values = np.array(possible_actions.values())
                        idx = values.argmax()
                        u_d[Position.C, mat, arrow, mm_state,
                            mm_health] = values[idx]

                        print(
                            f"({Position.C}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

        # south square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:
                        possible_actions = {}

                        def movementS(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        def gather(amount: int):
                            return u[Position.S, min(mat + amount, 2), arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            Action.UP: movementS(Position.C),
                            Action.STAY: movementS(Position.S)
                        })

                        # gather
                        possible_actions.update({
                            Action.GATHER: step_cost + 0.75 * gather(1) + 0.25 * gather(0)
                        })

                        values = np.array(possible_actions.values())
                        idx = values.argmax()
                        u_d[Position.S, mat, arrow, mm_state,
                            mm_health] = values[idx]

                        print(
                            f"({Position.S}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

        # east square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = {}

                        def movementE(new_pos: Position):
                            return step_cost + u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            Action.LEFT: movementE(Position.C),
                            Action.STAY: movementE(Position.E)
                        })

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                Action.SHOOT: step_cost + 0.1 * u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health] + 0.9 * (kill_reward + u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            })

                        # hit
                        if mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h50 or mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                Action.HIT: step_cost + 0.8 * u[Position.C, mat, arrow, mm_state, mm_health] + 0.2 * (
                                        kill_reward + u[Position.C, mat, arrow, mm_state, max(0, mm_health - 2)])
                            })

                        values = np.array(possible_actions.values())
                        idx = values.argmax()
                        u_d[Position.E, mat, arrow, mm_state,
                            mm_health] = values[idx]

                        print(
                            f"({Position.E}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")

        # west square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = {}

                        def movementW(new_pos: Position):
                            return step_cost + u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.update({
                            Action.RIGHT: movementW(Position.C),
                            Action.STAY: movementW(Position.W)
                        })

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.update({
                                Action.SHOOT: step_cost + 0.75 * u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health] + 0.25 * (kill_reward + u[
                                    Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            })

                        values = np.array(possible_actions.values())
                        idx = values.argmax()
                        u_d[Position.W, mat, arrow, mm_state,
                            mm_health] = values[idx]

                        print(
                            f"({Position.W}, {mat}, {arrow}, {mm_state}, {mm_health}):\
                            {list(possible_actions.keys())[int(idx)]}: [{values[idx]}]")


if __name__ == '__main__':
    main()
