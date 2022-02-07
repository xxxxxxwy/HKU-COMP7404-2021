"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack=util.Stack()
    # successor:(successor, action, stepCost)
    # stack:(node, path, Cost)
    node=problem.getStartState()
    path=[]
    cost=0
    stack.push([node,path,cost])
    explored=[]

    while not stack.isEmpty():
        [node,path,cost]=stack.pop()

        if problem.isGoalState(node):
            return path

        if not (node in explored):
            explored.append(node)
            for node1,action1,cost1 in problem.getSuccessors(node):
                cost2=cost+cost1
                path2=path+[action1]
                stack.push([node1,path2,cost2])

    #util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    queue=util.Queue()
    # successor:(successor, action, stepCost)
    # stack:(node, path, Cost)
    node=problem.getStartState()
    path=[]
    cost=0
    queue.push([node,path,cost])
    explored=[]

    while not queue.isEmpty():
        [node,path,cost]=queue.pop()

        if problem.isGoalState(node):
            return path

        if not (node in explored):
            explored.append(node)
            for node1,action1,cost1 in problem.getSuccessors(node):
                cost2=cost+cost1
                path2=path+[action1]
                queue.push([node1,path2,cost2])
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    Pqueue = util.PriorityQueue()#pop equal to heappop
    # successor:(successor, action, stepCost)
    # stack:(node, path, Cost)
    node = problem.getStartState()
    path = []
    cost = 0
    Pqueue.push([node, path, cost],0)
    explored = []

    while not Pqueue.isEmpty():
        [node, path, cost] = Pqueue.pop()

        if problem.isGoalState(node):
            return path

        if not (node in explored):
            explored.append(node)
            for node1, action1, cost1 in problem.getSuccessors(node):
                cost2 = cost + cost1
                path2 = path + [action1]
                Pqueue.push([node1, path2, cost2],cost2)
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    Pqueue = util.PriorityQueue()  # pop equal to heappop
    # successor:(successor, action, stepCost)
    # stack:(node, path, Cost)
    node = problem.getStartState()
    path = []
    cost = 0.0
    Pqueue.push([node, path, cost], 0)
    explored = []

    while not Pqueue.isEmpty():
        [node, path, cost] = Pqueue.pop()

        if problem.isGoalState(node):
            return path

        if not (node in explored):
            explored.append(node)
            for node1, action1, cost1 in problem.getSuccessors(node):
                cost2 = cost + cost1
                path2 = path + [action1]
                Pqueue.push([node1, path2, cost2], float(cost2)+heuristic(node1, problem))
    #util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
