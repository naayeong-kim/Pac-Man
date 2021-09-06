# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
from pacman import agents, gamestate, search, util

import ass2
import itertools


class CornersSearchRepresentation(search.SearchRepresentation):
    def __init__(self, gstate):
        super().__init__(gstate)
        self.walls = gstate.walls
        self.start_position = gstate.pacman
        left, bottom = 1, 1
        right, top = gstate.shape - 2 * util.Vector.unit
        self.corners = frozenset([util.Vector(left, bottom),
                                  util.Vector(left, top),
                                  util.Vector(right, bottom),
                                  util.Vector(right, top)])

    @property
    def start(self):
        # Tuple with as first element the position, and as second element
        # a tuple with one boolean per corner. This boolean is True
        # if the corner has been visited yet, False otherwise.
        # Initial corner check for completeness, in case we start in a corner.
        return self.start_position, self.check_corners(self.start_position, (False, False, False, False))

    def is_goal(self, state):
        # This will tell you the number of expanded nodes.
        # For example super().is_goal(state.vector) or super().is_goal(state[0])
        super().is_goal(state[0])
        return False not in state[1]

    def successors(self, state):
        # The position updates as usual.
        # Then we check whether we have reached any of the corners,
        # to get the new corner part of the search state
        successors = []
        for move in util.Move.no_stop:
            new_vector = state[0] + move.vector
            if not self.walls[new_vector]:
                new_visited = self.check_corners(new_vector, state[1])
                successor = ((new_vector, new_visited), [move], 1)
                successors.append(successor)
        return successors

    def check_corners(self, position, visited_corners):
        if position in self.corners:
            return tuple(visited or position == corner for visited, corner in zip(visited_corners, self.corners))
        else:
            return visited_corners

    def pathcost(self, path):
        return search.standard_pathcost(path, self.start_position, self.walls)


# Many choices are possible here, as long as they are admissible.
# Examples include the Manhattan distance to the closest corner, fastest corner, etc.
# It is also possible to use the costs of Manhattan paths from the player through
# all remaining corners, but admissibility must be ensured.
# An often-chosen but *inadmissible* heuristic is choosing a Manhattan path greedily.
# By trying all possible corner orders, we can ensure that there is no path
# with less cost than the returned heuristic value.
def corners_heuristic(state, representation):
    position, visited = state
    corners = [corner for corner, vis in zip(representation.corners, visited) if not vis]
    return min(manhattan_path_cost((position,) + corner_path) for corner_path in itertools.permutations(corners))


# Again, many choices possible, as long as they are admissible
# and not prohibitively inefficient. This heuristic is the same
# as the corners heuristic above, but for the foods closest to each corner
# rather than the corners themselves.
def dots_heuristic(state, representation):
    if state.dots:
        left, bottom = 1, 1
        right, top = representation.walls.shape - 2 * util.Vector.unit
        corners = frozenset([util.Vector(left, bottom), util.Vector(left, top),
                             util.Vector(right, bottom), util.Vector(right, top)])
        closest_to_corners = {min(state.dots, key=lambda dot: sum(abs(dot - corner))) for corner in corners}
        return min(manhattan_path_cost((state.vector,) + corner_path) for corner_path in
                   itertools.permutations(closest_to_corners))
    else:
        return 0

    # Some easier alternatives:
    return max(util.manhattan(state.vector, dot) for dot in state.dots)
    return len(state.dots.list())


def manhattan_path_cost(path):
    position = path[0]
    cost = 0
    for next_position in path[1:]:
        cost += util.manhattan(next_position, position)
        position = next_position
    return cost


class ClosestDotSearchAgent(agents.SearchAgent):
    def prepare(self, gstate):
        self.actions = []
        pacman = gstate.pacman
        while gstate.dots:
            next_segment = self.path_to_closest_dot(gstate)
            self.actions += next_segment
            for move in next_segment:
                if move not in gstate.legal_moves_vector(gstate.agents[self.id]):
                    raise Exception('path_to_closest_dot returned an illegal move: {}, {}'.format(move, gstate))
                gstate.apply_move(self.id, move)

        print(f'[ClosestDotSearchAgent] path found with length {len(self.actions)}'
              f' and pathcost {search.standard_pathcost(self.actions, pacman, gstate.walls)}')

    @staticmethod
    def path_to_closest_dot(gstate):
        return ass2.breadthfirst(AnyDotSearchRepresentation(gstate))


class AnyDotSearchRepresentation(search.PositionSearchRepresentation):
    def __init__(self, gstate):
        super().__init__(gstate)
        self.dots = gstate.dots

    def is_goal(self, state):
        return self.dots[state.x, state.y]


class ApproximateSearchAgent(agents.SearchAgent):
    def prepare(self, gstate: gamestate.Gamestate):
        pass

    def move(self, gstate: gamestate.Gamestate):
        raise exceptions.EmptyBonusAssignmentError
