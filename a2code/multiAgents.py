from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        food_list = newFood.asList()
        current_food_list = prevFood.asList()
        ghost_list = []
        for ghost in newGhostStates:
            ghost_list.append(ghost.getPosition())

        if (newPos in ghost_list) and (newScaredTimes[0] == 0):
            return -1
        if newPos in current_food_list:
            return 1

        def get_distance(x1, y1, x2, y2):
            # mhd distance
            return abs(x1 - x2) + abs(y1 - y2)

        min_food_dis = 999999
        for food in food_list:
            dis = get_distance(newPos[0], newPos[1], food[0], food[1])
            if dis < min_food_dis: min_food_dis = dis

        min_ghost_dis = 999999
        for ghost in ghost_list:
            dis = get_distance(newPos[0], newPos[1], ghost[0], ghost[1])
            if dis < min_ghost_dis: min_ghost_dis = dis

        # is this optimal?
        value = 1 / min_food_dis - 1 / min_ghost_dis

        return value


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ghost_id = []
        for i in range(1, gameState.getNumAgents()):
            ghost_id.append(i)

        # ghost_id:1,2,3,4....... pacman 0

        # ghost:
        def min_value(state, depth, ghost):
            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # v<---(inf)
            v = 999999

            for action in state.getLegalActions(ghost):

                # from the first ghost
                if ghost < ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = min(v, min_value(res, depth, ghost + 1))

                # all ghost finish
                elif ghost == ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = min(v, max_value(res, depth + 1))

            return v

        # pacman
        def max_value(state, depth):
            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # v<---(-inf)
            v = -999999

            for action in state.getLegalActions(0):
                # only one pacman
                res = state.generateSuccessor(0, action)
                v = max(v, min_value(res, depth, 1))

            return v

        res_list = []
        for action in gameState.getLegalActions(0):
            # pacman action list
            start = min_value(gameState.generateSuccessor(0, action), 0, 1)
            res_list.append((action, start))

        # sort by value
        res_list.sort(key=lambda res: res[1])

        return res_list[-1][0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghost_id = []
        for i in range(1, gameState.getNumAgents()):
            ghost_id.append(i)

        # ghost_id:1,2,3,4....... pacman 0

        # ghost:
        def min_value(state, depth, ghost, alpha=-999999, beta=999999):

            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # v<---(inf)
            v = 999999

            for action in state.getLegalActions(ghost):

                # from the first ghost
                if ghost < ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = min(v, min_value(res, depth, ghost + 1, alpha, beta))
                    if v < alpha: return v  # why cant equal???
                    beta = min([beta, v])
                # all ghost finish
                elif ghost == ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = min(v, max_value(res, depth + 1, alpha, beta))
                    if v < alpha: return v
                    beta = min([beta, v])

            return v

        # pacman
        def max_value(state, depth, alpha=-999999, beta=999999):
            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # v<---(-inf)
            v = -999999

            for action in state.getLegalActions(0):
                # only one pacman
                res = state.generateSuccessor(0, action)
                v = max(v, min_value(res, depth, 1, alpha, beta))
                if v > beta: return v
                alpha = max([alpha, v])

            return v

        next_v = -999999
        next_action = gameState.getLegalActions(0)[0]
        alpha = -999999
        beta = 999999

        for action in gameState.getLegalActions(0):
            v = min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if v > next_v:
                next_v, next_action = v, action
            alpha = max([alpha, next_v])
        return next_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghost_id = []
        for i in range(1, gameState.getNumAgents()):
            ghost_id.append(i)

        # ghost_id:1,2,3,4....... pacman 0

        # ghost:
        def min_value(state, depth, ghost):
            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            action_num = len(state.getLegalActions(ghost))
            sum = 0

            for action in state.getLegalActions(ghost):

                # from the first ghost
                if ghost < ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = min_value(res, depth, ghost + 1)

                # all ghost finish
                elif ghost == ghost_id[-1]:
                    res = state.generateSuccessor(ghost, action)
                    v = max_value(res, depth + 1)

                sum += v

            return sum / action_num

        # pacman
        def max_value(state, depth):
            # is terminal state
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            # v<---(-inf)
            v = -999999

            for action in state.getLegalActions(0):
                # only one pacman
                res = state.generateSuccessor(0, action)
                v = max(v, min_value(res, depth, 1))

            return v

        res_list = []
        for action in gameState.getLegalActions(0):
            # pacman action list
            start = min_value(gameState.generateSuccessor(0, action), 0, 1)
            res_list.append((action, start))

        # sort by value
        res_list.sort(key=lambda res: res[1])

        return res_list[-1][0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()

    food_list = newFood.asList()
    ghost = newGhostStates[0]
    score = currentGameState.getScore()

    a=12
    b=11

    def get_distance(x1, y1, x2, y2):
        # mhd distance
        return abs(x1 - x2) + abs(y1 - y2)

    min_food_dis = 999999
    for food in food_list:
        dis = get_distance(newPos[0], newPos[1], food[0], food[1])
        if dis < min_food_dis:
            min_food_dis = dis
    score += a / max(1, min_food_dis)

    #one ghost only
    ghostPos = ghost.getPosition()
    dis = max(1, get_distance(newPos[0], newPos[1], ghostPos[0], ghostPos[1]))
    if ghost.scaredTimer > 0:
        dis = 999999
    score += b / dis

    return score


# Abbreviation
better = betterEvaluationFunction
