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

    while True:
        u[:] = u_d[:]

        # Centre square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = []

                        def movementC(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.extend(
                            [movement(Position.N), movement(Position.S), movement(Position.W), movement(Position.E),
                             movement(Position.C)])

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.append(
                                step_cost + 0.5 * u[Position.C, mat, arrow - 1, mm_state, mm_health] + 0.5 * (
                                    kill_reward + u[Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            )

                        # hit
                        if mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h50 or mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.append(
                                step_cost + 0.9 * u[Position.C, mat, arrow, mm_state, mm_health] + 0.1 * (
                                    kill_reward + u[Position.C, mat, arrow, mm_state, max(0, mm_health - 2)])
                            )

                        u_d[Position.C, mat, arrow, mm_state,
                            mm_health] = max(possible_actions)

        # north square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = []

                        def movementN(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        def craft(arrows: int):
                            return u[Position.N, mat - 1, min(3, arrow + arrows), mm_state, mm_health]

                        # movement
                        possible_actions.extend(
                            [movementN(Position.C), movementN(Position.N)])

                        # craft
                        if mat > 0:
                            possible_actions.append(
                                step_cost + 0.5 * craft(1) + 0.35 * craft(2) + 0.15 * craft(3))

                        u_d[Position.N, mat, arrow, mm_state,
                            mm_health] = max(possible_actions)

        # south square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = []

                        def movementS(new_pos: Position):
                            return step_cost + 1 * u[new_pos, mat, arrow, mm_state, mm_health] + 0 * u[
                                Position.E, mat, arrow, mm_state, mm_health]

                        def gather(amount: int):
                            return u[Position.S, min(mat + amount, 2), arrow, mm_state, mm_health]

                        # movement
                        possible_actions.extend(
                            [movementS(Position.C), movementS(Position.S)])

                        # gather
                        possible_actions.append(
                            step_cost + 0.75 * gather(1) + 0.25 * gather(0))

                        u_d[Position.S, mat, arrow, mm_state,
                            mm_health] = max(possible_actions)

        # east square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = []

                        def movementE(new_pos: Position):
                            return step_cost + u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.extend(
                            [movementE(Position.C), movementE(Position.E)])

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.append(
                                step_cost + 0.1 * u[Position.C, mat, arrow - 1, mm_state, mm_health] + 0.9 * (
                                    kill_reward + u[Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            )

                        # hit
                        if mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h50 or mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.append(
                                step_cost + 0.8 * u[Position.C, mat, arrow, mm_state, mm_health] + 0.2 * (
                                    kill_reward + u[Position.C, mat, arrow, mm_state, max(0, mm_health - 2)])
                            )

                        u_d[Position.E, mat, arrow, mm_state,
                            mm_health] = max(possible_actions)

        # west square
        for mat in [0, 1, 2]:
            for arrow in [0, 1, 2, 3]:
                for mm_state in MMState:
                    for mm_health in MMHealth:

                        possible_actions = []

                        def movementW(new_pos: Position):
                            return step_cost + u[new_pos, mat, arrow, mm_state, mm_health]

                        # movement
                        possible_actions.extend(
                            [movementW(Position.C), movementW(Position.W)])

                        # shoot
                        if arrow > 0 and mm_health > 0:
                            kill_reward = 0
                            if mm_health == MMHealth.h25:
                                kill_reward = 50

                            possible_actions.append(
                                step_cost + 0.75 * u[Position.C, mat, arrow - 1, mm_state, mm_health] + 0.25 * (
                                    kill_reward + u[Position.C, mat, arrow - 1, mm_state, mm_health - 1])
                            )

                        u_d[Position.W, mat, arrow, mm_state,
                            mm_health] = max(possible_actions)


if __name__ == '__main__':
    main()
