"""
This file contains code that determines the behaviour of the pacman command line interface.
You can run this file using `python run.py [arguments]`. For example you can get help by using `python run.py -h`.

In general all commands are of the following form:

```
python run.py [global parameters] [mode] [mode parameters]
```

The global parameters can be any combination of:

- `-l` or `--layout`
- `-z` or `--zoom`
- `-s` or `--speed`
- `-d` or `--display`, can be `graphical`, `terminal` or `no`
- `-t` or `--timeouts`, enables computation timeouts on agents
- `-n` or `--runs`, the amount of repeated runs
- `-g` or `--ghosts`, the amount of ghosts

The mode can be one of `keyboard`, `search`, `reflex`, `adverserial` or `contest`.
The mode parameters depend on the chosen mode.
"""

import argparse
import os
import re
import sys

import pacman
import ass2
import ass3
import ass4
import ass5contest

# the directory of the layout files
LAYOUT_FILES_DIR = 'pacman/layout_files'

# the names of all the layout files
layout_names = [os.path.splitext(f)[0] for f in os.listdir(LAYOUT_FILES_DIR)]
contest_layouts = [layout for layout in layout_names if layout.startswith("contestLevel")]

# all available display types
display_types = {'no': pacman.displays.NoDisplay,
                 'terminal': pacman.displays.TerminalDisplay,
                 'graphical': pacman.displays.GraphicalDisplay}

# all available directional agents
direction_agents = {'left': pacman.agents.GoLeftAgent,
                    'right': pacman.agents.GoRightAgent}

# all available search agents
search_agents = {'search': pacman.agents.SearchAgent,
                 'stayleft': pacman.agents.StayLeftSearchAgent,
                 'stayright': pacman.agents.StayRightSearchAgent,
                 'closestdot': ass3.ClosestDotSearchAgent,
                 'approximate': ass3.ApproximateSearchAgent}

# all available search representations
search_representations = {'position': pacman.search.PositionSearchRepresentation,
                          'alldot': pacman.search.AllDotSearchRepresentation,
                          'crossroad': ass2.CrossroadSearchRepresentation,
                          'corners': ass3.CornersSearchRepresentation,
                          'anydot': ass3.AnyDotSearchRepresentation}

# all available search methods
search_methods = {'cheating': pacman.search.cheating,
                  'depthfirst': ass2.depthfirst,
                  'breadthfirst': ass2.breadthfirst,
                  'uniformcost': ass2.uniformcost,
                  'astar': ass2.astar}

# all available search heuristicsagentspacman
search_heuristics = {'null': pacman.search.null,
                     'manhattan': pacman.search.manhattan,
                     'euclidean': pacman.search.euclidean,
                     'corners': ass3.corners_heuristic,
                     'dots': ass3.dots_heuristic}

# all available reflex agents
reflex_agents = {'score': pacman.agents.ScoreReflexAgent,
                 'better': ass4.BetterReflexAgent}

# all available adverserial agents
adverserial_agents = {'minimax': ass4.MinimaxAgent,
                      'alphabeta': ass4.AlphabetaAgent,
                      'multialphabeta': ass4.MultiAlphabetaAgent}

# all available adverserial evaluation functions
adverserial_evaluates = {'score': pacman.agents.score_evaluate,
                         'better': ass4.better_evaluate}


def run(layout_name: str, pacman_agent: pacman.agents.PacmanAgent, display: pacman.displays.Display,
        speed: float, num_ghosts: int, timeouts: bool):
    """
    Run a single game of pacman.
    :param layout_name: the name of the layout to use
    :param pacman_agent: the already instantiated pacman agent to use
    :param display: the already instantiated display to use
    :param speed: the speed at which to run the game
    :param num_ghosts: the number of ghosts to use
    :param timeouts: whether to make use of agent action timeouts
    :return: the final Gamestate
    """
    layout, ghosts = pacman.layouts.load_layout(layout_name)
    num_ghosts = min(num_ghosts, len(ghosts))
    for _, position in ghosts[num_ghosts:]:  # remove superfluous ghosts
        layout[position] = pacman.layouts.LayoutObject.empty

    ghost_agents = [ghosts[i][0].agent(i + 1) for i in range(num_ghosts)]  # create ghost agents of correct type
    agents = [pacman_agent] + ghost_agents
    gstate = pacman.game.run_game(layout, agents, display, speed, timeouts)
    return gstate


def main():
    # global arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--layout', choices=layout_names, default=None, metavar='LAYOUT',
                        help='the name of the layout to use (without extension)')
    parser.add_argument('-z', '--zoom', default=1, type=float,
                        help='the zoom level, determines the size of the display')
    parser.add_argument('-s', '--speed', default=1, type=float,
                        help='the speed at which the game is run')
    parser.add_argument('-d', '--display', choices=display_types, default='graphical',
                        help='the display type to use')
    parser.add_argument('-t', '--timeouts', action='store_true',
                        help='whether to use agent action timeouts')
    parser.add_argument('-n', '--runs', default=1, type=int,
                        help='the amount of times to run the game with these options')
    parser.add_argument('-g', '--ghosts', default=100, type=int,
                        help='the maximum number of ghosts to place (actual number depends on layout)')

    # modes / subparsers
    subparsers = parser.add_subparsers(dest='mode')
    subparsers.add_parser('keyboard')
    direction_parser = subparsers.add_parser('direction')
    search_parser = subparsers.add_parser('search')
    reflex_parser = subparsers.add_parser('reflex')
    adverserial_parser = subparsers.add_parser('adverserial')
    subparsers.add_parser('contest')

    # direction arguments
    direction_parser.add_argument('direction', choices=direction_agents,
                                  help='the direction for the agent to move in')

    # search arguments
    search_parser.add_argument('-a', '--agent', choices=search_agents, default='search',
                               help='the search agent to use')
    search_parser.add_argument('-r', '--representation', choices=search_representations, default='position',
                               help='the search representation to use')
    search_parser.add_argument('-m', '--method', choices=search_methods, default='cheating',
                               help='the search method to use')
    search_parser.add_argument('-e', '--heuristic', choices=search_heuristics, default=None,
                               help='the search heuristic to use')

    # reflex arguments
    reflex_parser.add_argument('-a', '--agent', choices=reflex_agents, default='score',
                               help='the reflex agent to use')

    # adverserial arguments
    adverserial_parser.add_argument('-a', '--agent', choices=adverserial_agents, default='minimax',
                                    help='the adverserial agent to use')
    adverserial_parser.add_argument('-d', '--depth', default=2, type=int,
                                    help='the search depth to use')
    adverserial_parser.add_argument('-e', '--evaluate', default='score',
                                    help='the evaluation function to use')

    # ask the user for arguments if none passed
    if len(sys.argv) == 1:
        sys.argv.extend([x for x in re.split(r' +', input("Enter command-line arguments: ")) if x != ''])

    # preparation
    args = parser.parse_args()
    terminal = sys.stdout.isatty()

    # process --display
    display_type = display_types[args.display]
    if display_type == pacman.displays.TerminalDisplay and not terminal:
        display_type = pacman.displays.NoDisplay
    display = display_type(1 / args.zoom)

    # process --layout
    if args.layout:
        layouts = [args.layout]
    else:
        layouts = ['mediumClassic']  # default level

    # process mode / subparser
    if not args.mode or args.mode == 'keyboard':
        if display_type == pacman.displays.NoDisplay:
            raise Exception('cannot use keyboard without display')
        pacman_agent = pacman.agents.KeyboardAgent(display)

    elif args.mode == 'direction':
        agent_type = direction_agents[args.direction]
        pacman_agent = agent_type()

    elif args.mode == 'search':
        representation = search_representations[args.representation]
        agent_type = search_agents[args.agent]
        if args.heuristic:
            heuristic = search_heuristics[args.heuristic]
            method = lambda state: search_methods[args.method](state, heuristic)
            method.__name__ = 'astar'
        else:
            method = search_methods[args.method]
        pacman_agent = agent_type(representation, method)

    elif args.mode == 'reflex':
        agent_type = reflex_agents[args.agent]
        pacman_agent = agent_type()

    elif args.mode == 'adverserial':
        evaluate = adverserial_evaluates[args.evaluate]
        agent_type = adverserial_agents[args.agent]
        pacman_agent = agent_type(args.depth, evaluate)

    elif args.mode == 'contest':
        pacman_agent = ass5contest.ContestAgent()
        if not args.layout:  # no layout specified
            layouts = contest_layouts

    else:
        raise Exception('invalid mode passed')

    # Prepare statistics
    scores = []
    wins = []

    # run game
    for i in range(args.runs):
        for layout in layouts:
            # Indicate which run/layout we are on if needed
            if args.runs > 1:
                print(f'({i+1}/{args.runs}) ', end='')
            if len(layouts) > 1:
                print(f'{layout}: ', end='')

            # Run game
            gstate = run(layout, pacman_agent, display, args.speed, args.ghosts, args.timeouts)

            # Record results
            scores.append(gstate.score)
            wins.append(gstate.win)

            # Report results
            if gstate.win:
                print(f'Pacman emerges victorious! Score: {gstate.score}')
            else:
                print(f'Pacman died! Score: {gstate.score}')

    # Report statistics if applicable
    if len(scores) > 1:
        if args.mode == 'contest' and len(layouts) > 1:
            print(f'\nContest score: {sum(scores)/args.runs}')
        else:
            print(f'\nAverage score: {sum(scores)/len(scores)}')

        print(f'Wins: {wins.count(True)}/{len(wins)} ({int(100*wins.count(True)/len(wins))}% win rate)')


if __name__ == '__main__':

    main()
