# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

### Imports

import util

### Parameters

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever. It's just for psuedocode translation. 
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

### Search Strategies

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Searches the deepest nodes in the search tree first. Making sure to implement a graph search algorithm (with an explored set) instead of just Tree search. 

    Inputs:
    ----
    problem: A problem to search through and setup. 
    
    Returns:
    ----
    path: list of actions actions that reach the goal state.  

    To get started, might want to try some of these simple commands to understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # Intialize the frontier using a Stack queue data type (LIFO) 
    frontier = util.Stack()
    # Intialize the explored region:
    explored = set()

    # Push the root node to the frontier, in the form: node.state, node.actions
    frontier.push((problem.getStartState(),[]))

    # while it's not empty
    while not frontier.isEmpty():

        # pop the last-in leaf from the frontier
        node, actions = frontier.pop()

        # Get the successors of the nodes 
        for coord, direction, steps in problem.getSuccessors(node):
            #print coord, direction, steps
            # Check if the new leaf is in visited
            if not coord in explored:
                # if the leaf node is the goal state
                if problem.isGoalState(coord):
                    # we are done, return the list of actions that got us to this susccesful node
                    # Without the last direction, never completes, so push that last direction into the list of actions for this node
                    # If we find a goal node, we return all the actions taken to this node (lookup frontier for goal node)
                    return actions + [direction]

                # Else, update the frontier with the node, and actions taken to get to that node, and the new direction
                frontier.push((coord, actions + [direction]))
                # And update the explored region
                explored.add(coord)
    # Else return empty list of actions            
    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    frontier = util.Queue()
    frontier.push( (problem.getStartState(), []) )
    visited = []
    while not frontier.isEmpty():
        node, actions = frontier.pop()
        for coord, direction, steps in problem.getSuccessors(node):
            if not coord in visited:
                if problem.isGoalState(coord):
                    return actions + [direction]
                frontier.push((coord, actions + [direction]))
                visited.append(coord)
    return []


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    frontier = util.PriorityQueue()
    frontier.push( (problem.getStartState(), []), 0)
    visited = []
    while not frontier.isEmpty():
        node, actions = frontier.pop()
        if problem.isGoalState(node):
            return actions
        visited.append(node)
        for coord, direction, steps in problem.getSuccessors(node):
            if not coord in visited:
                new_actions = actions + [direction]
                frontier.push((coord, new_actions), problem.getCostOfActions(new_actions))
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."    
    visited = []
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start,[]), heuristic(start, problem))
    while not frontier.isEmpty():
        node, actions = frontier.pop()
        if problem.isGoalState(node):
            return actions
        visited.append(node)
        for coord, direction, cost in problem.getSuccessors(node):
            if not coord in visited:
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                frontier.push( (coord, new_actions), score)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
