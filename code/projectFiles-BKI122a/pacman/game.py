"""
This file contains code for actually running a game of Pacman.
"""

import collections
import time
from typing import List

from pacman import agents, array, displays, gamestate, tech_util

# some constants are defined here that have to do with timeouts
PREPARE_TIMEOUT = 15  # seconds
MOVE_TIMEOUT = 3  # seconds
MOVE_WARNING = 1  # seconds
MAX_WARNINGS = 3  # times


def run_game(layout: array.Array, all_agents: List[agents.Agent], display: displays.Display,
             speed: float = 1, timeouts: bool = True):
    """
    Run a game of pacman.
    :param layout: layout to use
    :param all_agents: list of agents to use, first of which is Pacman
    :param display: the display to use
    :param speed: the speed to use
    :param timeouts: whether to use agent move timeouts
    """
    # create initial gamestate
    gstate = gamestate.Gamestate(layout)

    # let agents prepare
    for agent in all_agents:
        if timeouts:
            agent_prepare_timeout(agent, gstate)
        else:
            agent.prepare(gstate.copy)

    # initialise the display
    pacman: agents.PacmanAgent = all_agents[0]
    display.initialise(gstate.copy, pacman.cell_values)
    display.show(gstate.copy)

    # initialise timeout warning counter
    timeout_warnings = collections.Counter()

    # main game loop
    while not gstate.gameover:
        # ask each agent that can move for their next move and apply it to the gamestate
        for agent in all_agents:
            if gstate.can_move(agent.id):
                if timeouts:
                    move = agent_move_timeout(agent, gstate, timeout_warnings)
                else:
                    move = agent.move(gstate.copy)
                gstate.apply_move(agent.id, move)

        gstate.tick()
        display.show(gstate.copy)
        time.sleep(display.preferred_timedelta / speed)

    # reset display
    display.reset()

    return gstate.copy


def agent_prepare_timeout(agent: agents.Agent, gstate: gamestate.Gamestate):
    """
    Let agent prepare, while applying timeouts
    """
    try:
        with tech_util.timeout(PREPARE_TIMEOUT):
            agent.prepare(gstate.copy)
    except tech_util.TimeoutException:
        gstate.destroy(agent.id)
        print(f'WARNING! agent {agent.id} reached prepare timeout of {PREPARE_TIMEOUT} seconds and was destroyed')


def agent_move_timeout(agent: agents.Agent, gstate: gamestate.Gamestate, timeout_warnings: collections.Counter):
    """
    Let agent calculate their next move, while applying timeouts
    """
    timeit = None
    try:
        with tech_util.timeit() as timeit, tech_util.timeout(MOVE_TIMEOUT):
            return agent.move(gstate.copy)
    except tech_util.TimeoutException:
        gstate.destroy(agent.id)
        print(f'WARNING! agent {agent.id} reached move timeout of {MOVE_TIMEOUT} seconds and was destroyed')
    finally:
        if timeit and timeit.t >= MOVE_WARNING:
            timeout_warnings[agent.id] += 1
            print(f'WARNING! agent {agent.id} took more than {MOVE_WARNING} seconds to move, '
                  f'agent now has {timeout_warnings[agent.id]} warning(s)')
            if timeout_warnings[agent.id] >= MAX_WARNINGS:
                gstate.destroy(agent.id)
                print(f'WARNING! agent {agent.id} was warned {MAX_WARNINGS} times and was destroyed')
