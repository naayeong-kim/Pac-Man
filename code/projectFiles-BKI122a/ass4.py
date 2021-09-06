# enter your names and student numbers below
# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)

from pacman import agents, gamestate, util


class BetterReflexAgent(agents.ReflexAgent):
    def evaluate(self, gstate, move):
        gstate.apply_move(0, move)

        score = 0
        dotsNotEaten = 0
        pelletsNotEaten = 0

        dotList = []    # list to store distances between pacman and food/dots
        ghostList = []  # list to store distances between pacman and ghosts
        pelletList = [] # list of stored pellet positions and to store the distances between pacman and pellets

        # to encourage a win or to avoid a loss pacman needs to get the highest or lowest possible scores
        if gstate.win:
            return float('inf')
        elif gstate.loss:
            return float('-inf')

        # we create for every dot/food a minus score so that when pacman eats the dot the score becomes higher resulting
        # in pacman becoming more encouraged to get to them faster resulting in a faster victory
        for dot in gstate.dots.list():
            dotDist = util.manhattan(gstate.pacman, dot)
            dotList.append(dotDist)
            dotsNotEaten -= 150

        # to fill the ghostList with the distances between pacman and ghost and to encourage pacman to eat ghost after
        #  it has eaten a pellet by getting a higher score when it is closer to a ghost
        for ghost in gstate.ghosts:
            ghostDist = util.manhattan(gstate.pacman, ghost)
            ghostList.append(ghostDist)
            if gstate.timers != 0 and ghostDist != 0:
                if ghostDist < 2:
                    score += (1 / ghostDist) * 200

        # to fill the pelletList we add the tuple (pellet position, distance) for each pellet in maze
        for pellet in gstate.pellets.list():
            pelletList.append((pellet, util.manhattan(gstate.pacman, pellet)))

        # to encourage pacman to eat the pellets it gets a higher score when it is closer to a pellet and
        # when it has eaten one
        for pelletPos, pelletDist in pelletList:
            score += (1 / pelletDist) * 500
            if gstate.pacman == pelletPos:
                score += 1200
            pelletsNotEaten -= 800

        # to encourage pacman to stay away from ghosts and to get closer to food, the score decreases
        #  when it comes closer to ghosts and increases when it comes closer to food and to discourage pacman
        # to stay too lang in one position, the move stop decreases the score
        for distance in ghostList:
            score -= (1 / distance) * 600
            if move.stop:
                score -= 50
        for distance in dotList:
            score += (1 / distance) * 100
            if move.stop:
                score -= 150

        return score + dotsNotEaten + pelletsNotEaten


class MinimaxAgent(agents.AdversarialAgent):
    def move(self, gstate):

        # Function that obtains the largest maximum value among the minimum values , deciding the movement of pacman
        def maximizer(state: gamestate.Gamestate, depth):
            if depth == self.depth or state.win or state.loss:
                return self.evaluate(state)
            # Sets maxVal to infinite number to find the maximum score by comparing it to other values
            maxVal = float('-inf')
            # Adds all possible movements of the current state to list
            moveList = state.legal_moves_vector(state.pacman)
            # It returns the maximum value of all the successors in the current state
            for action in moveList:
                maxVal = max(maxVal, minimizer(state.successor(0, action), depth, 1))
            return maxVal

        # Function that returns the smallest value among the maximum values deciding the movement of the ghosts
        def minimizer(state: gamestate.Gamestate, depth, agentIdx):
            if depth == self.depth or state.win or state.loss:
                return self.evaluate(state)
            # Sets minVal to infinite negative number to find the minimum score by comparing it to other values
            minVal = float('inf')
            # Adds all possible movements in current state to list
            moveList = state.legal_moves_id(agentIdx)

            # For the last agent:
            if agentIdx == len(state.active_agents) - 1:
                # For the successors of current state and agent, choose the smallest value
                for action in moveList:
                    minVal = min(minVal, maximizer(state.successor(agentIdx, action), depth + 1))
            # In the case it is not a last agent:
            else:
                # For the successors of current state and agent, choose the smallest value
                for action in moveList:
                    minVal = min(minVal, minimizer(state.successor(agentIdx, action), depth, agentIdx + 1))
            return minVal

        # to remove the move stop from possible actions of pacman
        moves = []
        for move in gstate.legal_moves_id(self.id):
            if move is not util.Move.stop:
                moves.append(move)

        # for all possible actions that pacman can take, it returns the action that gives highest score for pacman
        val = float('-inf')
        for action in moves:
            temp = minimizer(gstate.successor(0, action), 0, 1)
            if temp > val: # Compares among the minimum values to choose the maximum value
                val = temp
                move = action
        print(val)
        return move



class AlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        def maximizer(state, depth, alpha, beta):
            if state.loss or state.win or depth == 0:
                return self.evaluate(state)  # return evaluation function of current node if it will win or lose.
            else:
                value = float('-inf')
                moves = []

                for move in state.legal_moves_id(0):  # add all moves of pacman
                    if move is not util.Move.stop:  # except stop move
                        moves.append(move)

                for move in moves:
                    score = minimizer(state.successor(0, move), depth, alpha, beta)
                    if score > value:
                        value = score  # update score if new score is better than best score
                    alpha = max(alpha, value)  # update alpha with max of current alpha and best core
                    if beta <= alpha:
                        break  # prune if beta is smaller than alpha
                return value  # return best score

        def minimizer(state, depth, alpha, beta):
            if state.loss or state.win or depth == 0:
                return self.evaluate(state)  # return evaluation function of current node if it will win or lose.
            else:
                value = float('inf')
                moves = []
                for move in state.legal_moves_id(1):  # add all moves of the ghost
                    if move is not util.Move.stop:  # except stop move
                        moves.append(move)

                for move in moves:
                    score = maximizer(state.successor(1, move), depth - 1, alpha, beta)
                    if score < value:  # update score if new score is better than best score
                        value = score
                    beta = min(beta, value)  # update beta with the min of beta and best score
                    if beta <= alpha:  # if beta is smaller than alpha, prune!
                        break
                return value  # return best score

        value = float('-inf')  # best score for now is really low
        alpha = float('-inf')  # alpha is low
        beta = float('inf')  # beta is high
        moves = []  # create list for moves

        for move in gstate.legal_moves_id(self.id):  # add all pacman moves
            if move is not util.Move.stop:  # only if it is not a stop move
                moves.append(move)

        best_move = moves[0]  # start with first move as best move

        for move in moves:
            score = minimizer(gstate.successor(0, move), self.depth, alpha, beta)  # calculate score
            if score > value:
                best_move = move  # if new score is better than best score, update move
                value = score  # and update score
        print(value)
        return best_move  # return best move


def better_evaluate(gstate: gamestate.Gamestate):
    dotList = []    # list to store distances between pacman position and dots
    pelletList = [] # list to store distances between pacman position and pellets

    score = 0
    dotsNotEaten = 0
    pelletsNotEaten = 0

    # to encourage a win or to avoid a loss pacman needs to get the highest or lowest possible scores
    if gstate.win:
        return float('inf')
    elif gstate.loss:
        return float('-inf')

    # we create for every dot/food a minus score so that when pacman eats the dot the score becomes higher resulting
    # in pacman becoming more encouraged to get to them faster resulting in a faster victory
    for dot in gstate.dots.list():
        dotDist = util.manhattan(gstate.pacman, dot)
        dotList.append(dotDist)
        dotsNotEaten -= 180

    # to fill the pelletList we add the tuple (pellet position, distance) for each pellet in maze
    for pellet in gstate.pellets.list():
        pelletList.append((pellet, util.manhattan(gstate.pacman, pellet)))

    # to encourage pacman to eat the pellets it gets a higher score when it is closer to a pellet and
    # when it has eaten one
    for pelletPos, pelletDist in pelletList:
        score += (1 / pelletDist) * 500
        if gstate.pacman == pelletPos:
            score += 1200       # If pacman eat pellet, it will get high score
        pelletsNotEaten -= 800

    # to fill the ghostList with the distances between pacman and ghost and to encourage pacman to eat ghost after
    # it has eaten a pellet by getting a higher score when it is closer to a ghost and to decrease the score if it
    # has not eaten a pellet and it is is close to a ghost to avoid it
    for ghost in gstate.ghosts:
        ghostDist = util.manhattan(gstate.pacman, ghost)
        if gstate.timers != 0:
            if ghostDist < 2:
                score += (1 / ghostDist) * 1500
        else:
            score -= (1 / ghostDist) * 600

    # to encourage pacman to eat food/dots, the score increases if it comes closer to food
    for distance in dotList:
        score += (1 / distance) * 100

    return score + dotsNotEaten + pelletsNotEaten


class MultiAlphabetaAgent(agents.AdversarialAgent):
    def move(self, gstate):
        def maximizer(state: gamestate.Gamestate, depth, alpha, beta):
            if depth == 0 or state.loss or state.win:
                return self.evaluate(state)
            else:
                value = float('-inf')
                moveList = []

                for move in state.legal_moves_id(0):
                    if move is not util.Move.stop:
                        moveList.append(move)

                for move in moveList:
                    score = minimizer(state.successor(0, move), depth, alpha, beta, 1)
                    if score > value:
                        value = score
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break
                return value


        def minimizer(state: gamestate.Gamestate, depth, alpha, beta, ghostIdx):
            if depth == 0 or state.loss or state.win:
                return self.evaluate(state)
            else:
                value = float('inf')
                moveList = []
                for move in state.legal_moves_id(ghostIdx):
                    if move is not util.Move.stop:
                        moveList.append(move)

                for action in moveList:
                    if ghostIdx < len(state.ghosts):
                        value = minimizer(state.successor(ghostIdx, action), depth, alpha, beta, ghostIdx + 1)
                    else:
                        value = maximizer(state.successor(ghostIdx, action), depth - 1, alpha, beta)
                    beta = min(beta, value)
                    if beta <= alpha:  # prune
                        break
                return value

         # to remove the move stop from possible actions of pacman
        moves = []
        for move in gstate.legal_moves_id(self.id):
            if move is not util.Move.stop:
                moves.append(move)

        val = float('-inf')     # val is used to find maximum score
        alpha = float('inf')    # alpha is used to find minimum value in successors
        beta = float('-inf')    # beta is used to find maximum value in successors

        for action in moves:
            temp = minimizer(gstate.successor(0, action), self.depth, alpha, beta, 1)
            if temp > val:
                move = action
                val = temp
        print(f'score: {val}')
        return move