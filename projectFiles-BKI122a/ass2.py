# enter your names and student numbers below
# name1 (s0123456)
# name2 (s6543210)

import exceptions
from pacman import search, util

import queue


def depthfirst(representation):
    """
    Search the deepest nodes in the tree first.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", representation.start)
    print("Is the start a goal?", representation.is_goal(representation.start))
    print("Start's successors:", representation.successors(representation.start))
    """
    # The frontier contains the search states to visit: here, a last-in-first-out queue
    frontier = queue.LifoQueue()

    # For Pacman search problems, a search state is a position tuple (x,y), but correct
    # code should be able to work with any (hashable) search state.
    # A search node / successor is a tuple of the search state, the list of actions
    # performed so far, and the path cost so far.
    # Storing the entire list of actions is not the most efficient,
    # but it is easy to implement; an example of a more efficient implementation
    # stores each search node's "parent" and the last move taken, so that the path
    # can be reconstructed by tracing the search node's ancestors back till the start state.
    frontier.put((representation.start, [], 0))

    # Store the search states we have already visited. Sets only work when its elements
    # are hashable, so make sure this is the case when you want to use search for new problems.
    explored = set()

    while not frontier.empty():
        # Get the top (last-pushed) element from the frontier
        state, path, cost = frontier.get()

        # Make sure the state has not been visited before, and mark it as visited.
        if state in explored:
            continue
        explored.add(state)

        # Check whether we have reached the goal
        if representation.is_goal(state):
            return path

        # For all successors (tuples of a search state, list of actions taken, new actions' cost)
        for successorState, actions, actionCost in representation.successors(state):
            # This check is not necessary because of the above explored check,
            # but is implemented for efficiency reasons
            if successorState not in explored:
                # Add the new successor to the frontier
                frontier.put((successorState, path + actions, cost + actionCost))

    # If we run out of new nodes to try out without returning, then search hsa failed
    return None


def breadthfirst(representation):
    """
    Search the shallowest nodes in the search tree first
    """

    # Only difference: using a first-in-first-out Queue instead of the LifoQueue
    frontier = queue.Queue()
    frontier.put((representation.start, [], 0))

    explored = set()

    while not frontier.empty():
        state, path, cost = frontier.get()

        if state in explored:
            continue
        explored.add(state)

        if representation.is_goal(state):
            return path

        for successorState, actions, actionCost in representation.successors(state):
            if successorState not in explored:
                frontier.put((successorState, path + actions, cost + actionCost))

    return None


def uniformcost(representation):
    """
    Search the node of least total cost first.
    """
    # Only difference: using a priority queue instead of the LifoQueue
    # A priority queue pulls out an element based on the first tuple element (cost),
    # in case of a draw it falls back to the second element (the position), etc.
    # As we are not interested in tie-breaking behaviour here, this is fine.
    frontier = queue.PriorityQueue()
    frontier.put((0, (representation.start, [], 0)))

    explored = set()

    while not frontier.empty():
        _, successor = frontier.get()
        state, path, cost = successor

        if state in explored:
            continue
        explored.add(state)

        if representation.is_goal(state):
            return path

        for successorState, actions, actionCost in representation.successors(state):
            if successorState not in explored:
                frontier.put((cost + actionCost, (successorState, path + actions, cost + actionCost)))

    return None


def astar(representation, heuristic=search.null):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # Only difference: using a priority queue based on a function instead of a LifoQueue
    # Unlike UCS, where we could also have used this class as well, here the function
    # is the path cost so far plus the heuristic value of the state.
    frontier = util.PriorityFunctionQueue(
        lambda search_state: heuristic(search_state[0], representation) + search_state[2])

    frontier.put((representation.start, [], 0))
    explored = set()

    while not frontier.empty():
        state, path, cost = frontier.get()
        if state in explored:
            continue

        if representation.is_goal(state):
            return path

        explored.add(state)
        for successorState, actions, actionCost in representation.successors(state):
            if successorState not in explored:
                frontier.put((successorState, path + actions, cost + actionCost))

    return None


class CrossroadSearchRepresentation(search.PositionSearchRepresentation):
    def successors(self, state):
        """
        Returns a list of successors, which are (position, moves, cost) tuples.
        """
        successors = []
        for firstMove in self.legal_moves(state):  # for all initial moves
            position = state + firstMove.vector
            path = [firstMove]

            # Keep moving while we can only move onwards or turn back (no crossroads or dead end)
            next_moves = [move for move in self.legal_moves(position) if move != path[-1].opposite]
            while len(next_moves) == 1:
                position = position + next_moves[0].vector
                path.append(next_moves[0])
                next_moves = [move for move in self.legal_moves(position) if move != path[-1].opposite]

            successors.append((position, path, len(path)))

        return successors

    def legal_moves(self, position):
        moves = []
        for move in util.Move.no_stop:
            new_vector = position + move.vector
            if not self.walls[new_vector]:
                moves.append(move)
        return moves
