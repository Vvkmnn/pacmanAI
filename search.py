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

# Imports

import util

# Parameters


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

# Search Strategies

# Tiny Maze


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

# Depth First Search


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
    frontier.push((problem.getStartState(), []))

    # while it's not empty
    while not frontier.isEmpty():

        # pop the last-in leaf from the frontier
        node, actions = frontier.pop()

        # Check if the current node is the goal state
        if problem.isGoalState(node):
            # we are done, return the list of actions that got us to this succesful node
            # If we find a goal node, we return all the actions for this node
            # (which is stored in the frontier Stack)
            return actions

        # Get the successors of the nodes
        for coord, direction, steps in problem.getSuccessors(node):
            # print coord, direction, steps
            # Check if the new leaf is in visited
            if not coord in explored:
                # If not, update the frontier with the new node, actions taken
                # to get to that node, and the final direction
                frontier.push((coord, actions + [direction]))
                # Also update the explored region
                explored.add(coord)

    # Else return empty list of actions
    return []

# Breadth First Search


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first; guaranteed we'll find a solution, because we'll check every node eventually!

    Inputs:
    ----
    problem: A problem to search through and setup. 

    Returns:
    ----
    path: list of actions actions that reach the goal state.  
    """

    # This time, let's use a Queue data type (FIFO)
    frontier = util.Queue()
    # Initialize the explored region
    explored = set()

    # Push the root node to the frontier, in the form: node.state, node.actions
    frontier.push((problem.getStartState(), []))

    # while it's not empty
    while not frontier.isEmpty():
        # pop the FIRST leaf from the frontier (using FIFO)
        node, actions = frontier.pop()

        # And if it's a goal state
        if problem.isGoalState(node):
            # Return the list of actions that got us to that node
            return actions

        # If we are not done, get the successors of the node and for each
        # successor node, in every direction
        for coord, direction, steps in problem.getSuccessors(node):
            # If we've never been there
            if not coord in explored:
                # Otherwise push the new node into the frontier with the path
                # that got us there and the direction we need to reach that
                # successor
                frontier.push((coord, actions + [direction]))
                # Also update the explored region for Graph Search instead of
                # Tree Search
                explored.add(coord)
    return []

# Cheapest First Search


def uniformCostSearch(problem):
    """
    Search the nodes with the cheapest cost first; also known as cheapest first search.

    Inputs:
    ----
    problem: A problem to search through and setup. 

    Returns:
    ----
    path: list of actions actions that reach the goal state.  
    """

    # Now we use the priority Queue data type, where each element in the Queue
    # has a priority assigned to it at the outset; here the cost per step.
    frontier = util.PriorityQueue()
    # Initialize the explored region
    explored = set()

    # Push the root node to the frontier, in the form: node.state,
    # node.actions, node.cost
    frontier.push((problem.getStartState(), []), 0)

    # While the Priority Queue has options
    while not frontier.isEmpty():
        # Grab the node and history with the highest priority (lowest cost)
        node, actions = frontier.pop()

        # If the node is the goal state
        if problem.isGoalState(node):
            # Return the actions that got us here
            return actions

        # Else, let's start exploring Successors
        for coord, direction, steps in problem.getSuccessors(node):
            # If we've never seen it before
            if not coord in explored:
                # Use the convenient GetCostOfActions method to lookup the cost for this new history
                # That new path cost becomes the node.cost in the tree
                frontier.push((coord, actions + [direction]),
                              problem.getCostOfActions(actions + [direction]))
                # Also update the explored set
                explored.add(node)

    return []

### A* Search


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest goal in the provided SearchProblem. Used in aStarSearch, so defined prior. 

    For a trivial example, we will use one that returns a 0 every time. This is akin to saying all nodes are an equiavelent (0) distance to the goal; a heuristic that places all nodes on the same value.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first; best of both worlds! Defaults to the nullHeuristic, but more complex heuristics should provide better results. 

    Inputs:
    ----
    problem: A problem to search through and setup. 

    Returns:
    ----
    path: list of actions actions that reach the goal state.  
    """

    # Lets use the priority Queue data type again, because we need to know
    # path costs via priority.
    frontier = util.PriorityQueue()
    # Initialize the explored region
    explored = set()

    # This time, also initialize a root node so we can run the heuristic on it
    root = problem.getStartState()

    # Push the root node to the frontier, in the form: node.state, node.actions, node.cost
    # But now we are using the nullHeuristic function to return our path costs
    frontier.push((root, []), heuristic(root, problem))

    # While it's not empty
    while not frontier.isEmpty():
        # Grab the leaf with the highest priority
        node, actions = frontier.pop()

        # Is that the goal? If so, get us the history and be done
        if problem.isGoalState(node):
            return actions

        # No goal yet, let's get some successors
        for coord, direction, cost in problem.getSuccessors(node):
            # If it's not in the explored set
            if not coord in explored:

                # A* search has two components: g(n) + h(n)
                # g(n): The cost of the path from the root node to the current node
                # h(n): The heuristic estimate the cheapest path from the
                # current node to the goal node

                # The key here is h(n); we need an admissable heuristic (it must never overestimate the actual cost to get to the goal node)
                # It must be an optimistic heuristic; never overlooks the
                # possibility of cheaper nodes

                # Since the two components get summed up to approximate
                # cost/priority, we do that here:
                score = problem.getCostOfActions(actions + [direction]) + heuristic(coord, problem)
                # Let's push this into the Priority Queue with the cost AND the
                # heuristic distance value as the new score
                frontier.push((coord, actions + [direction]), score)
                # Also update the explored set
                explored.add(node)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
