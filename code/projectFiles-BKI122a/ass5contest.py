# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)

import exceptions
from pacman import agents, gamestate, util, distancer

import exceptions
import numbers
import random
from pacman import agents, gamestate, util
from pacman.distancer import Distancer


class ContestAgent(agents.PacmanAgent):
    """
    The code below specifies a totally moronic ContestAgent.
    It just moves to the neighbouring cell with the highest game score.
    It does not look ahead and does not even try to avoid ghosts.
    You can do far better!
    """

    def prepare(self, gstate):
        """
        Use this method for initializing tour ContestAgent.
        The provided stump only calls the prepare of the mother class.
        You might want to add other things, for instance
        calling the precompute_distances() method of the Distancer class
        """
        super().prepare(gstate)
        self.distancer = distancer.Distancer(gstate)
        self.distancer.precompute_distances()
        self.dotsList = gstate.dots.list()
        self.smallFood = 1/20 * len(self.dotsList)

    def move(self, gstate: gamestate.Gamestate) -> util.Move:
        """
        This method gets called every turn, asking the agent
        what move they want to make based on the current gamestate.
        """
        moves = gstate.legal_moves_vector(gstate.agents[self.id])
        scores = {move: self.evaluate(gstate.copy, move) for move in moves}
        max_score = max(scores.values())
        max_moves = [move for move in moves if scores[move] == max_score]
        return random.choice(max_moves)

    def evaluate(self, gstate: gamestate.Gamestate, move: util.Move):
        """
        This method is used by the reflex agent to determine
        the value of a given move if it would be used in a given gamestate.
        """
        score = gstate.score
        gstate.apply_move(0, move)

        dotsNotEaten = 0
        dotsPresent = 0
        pelletsNotEaten = 0

        dotList = []  # list to store distances between pacman and food/dots
        ghostList = []  # list to store distances between pacman and ghosts
        pelletList = []  # list of stored pellet positions and to store the distances between pacman and pellets

        # to encourage a win or to avoid a loss pacman needs to get the highest or lowest possible scores
        if gstate.win:
            return float('inf')
        elif gstate.loss:
            return float('-inf')

        # we create for every dot/food a minus score so that when pacman eats the dot the score becomes higher resulting
        # in pacman becoming more encouraged to get to them faster resulting in a faster victory. And we use an integer
        #  to see how many food dots are still present in level
        for dot in gstate.dots.list():
            dotDist = self.distancer.get_distance(gstate.pacman, dot)
            dotList.append((dot, dotDist))
            dotsPresent += 1


        # to fill the pelletList we add the tuple (pellet position, distance) for each pellet in maze
        for pellet in gstate.pellets.list():
            pelletList.append((pellet, self.distancer.get_distance(gstate.pacman, pellet)))

        # to encourage pacman to eat the pellets it gets a higher score when it is closer to a pellet and
        # when it has eaten one
        for pelletPos, pelletDist in pelletList:
            score += (1 / pelletDist) * 180
            pelletsNotEaten -= 150
            if gstate.pacman == pelletPos:
                score += 600

        # to encourage pacman to eat the dots it gets a higher score when it is closer to a dot and
        # when it has eaten one. In addition, if there is a small amount of food left in level then we increase score
        # decrease score when pacman stops moving
        for dotPos, distance in dotList:
            score += (1 / distance) * 600
            dotsNotEaten -= 800
            if gstate.pacman == dotPos:
                score += 500
                if dotsPresent < self.smallFood:
                    score += 1000
            if move is move.stop:
                score -= 700

        # to fill the ghostList with the distances between pacman and ghost and to encourage pacman to eat ghost after
        # it has eaten a pellet by getting a higher score when it is closer to a ghost. And to decrease score when
        # ghosts are not scared so that pacman avoids them. And make pacman less scared of ghosts when there is a small
        # amount of food left in level
        for ghost in gstate.ghosts:
            ghostDist = self.distancer.get_distance(gstate.pacman, ghost)
            ghostList.append(ghostDist)

            for timer in gstate.timers:
                # In the case of the ghost are scared and there is enough time left
                if timer >= 4:
                    # If pacman can eat ghost, give a high score
                    if ghostDist == 0:
                        score += 6000
                    # if pacman is very close to ghost, encourage pacman to chase ghost
                    elif ghostDist < 2:
                        score += 300
                    # If there is enough time to eat the ghost, encourge pacman to go to ghost
                    elif ghostDist < timer:
                        score += (1 / ghostDist) * 300
                #In the case that the ghost are not scared or there is not enought time left to chase ghosts
                elif timer < 4 and ghostDist != 0:
                    # To make pacman less scared when there is little food
                    if dotsPresent < self.smallFood:
                        # If ghost is close to make pacman avoid them quickly
                        if ghostDist < 3:
                            score -= (1 / ghostDist) * 1000
                        else:
                            score -= (1 / ghostDist) * 100
                    # If ghosts are not scared and there is enough food left in level
                    else:
                        # If ghost is close to make pacman avoid them quickly
                        if ghostDist < 3:
                            score -= (1 / ghostDist) * 2000
                        else:
                            score -= (1 / ghostDist) * 400

        return score + dotsNotEaten + pelletsNotEaten

    def successors(self, gstate, state):
        """
        Returns a list of successors, which are (position, moves, cost) tuples.
        """
        successors = []
        for firstMove in self.legal_moves(gstate, state):  # for all initial moves
            position = state + firstMove.vector
            path = [firstMove]

            # Keep moving while we can only move onwards or turn back (no crossroads or dead end)
            next_moves = [move for move in self.legal_moves(gstate, position) if move != path[-1].opposite]
            while len(next_moves) == 1:
                position = position + next_moves[0].vector
                path.append(next_moves[0])
                next_moves = [move for move in self.legal_moves(gstate, position) if move != path[-1].opposite]

            successors.append((position, path, len(path)))

        return successors

    def legal_moves(self, gstate: gamestate.Gamestate, position):
        moves = []
        for move in util.Move.no_stop:
            new_vector = position + move.vector
            if not gstate.walls[new_vector]:
                moves.append(move)
        return moves